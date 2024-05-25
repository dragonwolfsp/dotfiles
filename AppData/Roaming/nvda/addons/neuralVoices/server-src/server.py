synth = None
srvHandle = None
server_exit = False
import sys
from ctypes import byref
import os
import ctypes
import threading
ctypes.windll.ole32.CoInitialize(0)
import azure.cognitiveservices.speech as sdk
from azure.cognitiveservices.speech.enums import *
from azure.cognitiveservices.speech.audio import *
from serial.win32 import FILE_FLAG_OVERLAPPED, OVERLAPPED, LPOVERLAPPED, CreateEvent, ERROR_IO_PENDING, GetOverlappedResult
import time
import json
import logging
logging.basicConfig(level=logging.INFO)

ERROR_MORE_DATA = 234
ERROR_PIPE_CONNECTED = 535
MSG_SPEECH_STARTED = 1
MSG_AUDIO = 2
MSG_MARK = 3
MSG_SPEECH_COMPLETED = 4
MSG_VOICES = 5
#C2S
MSG_SPEAK = 0
MSG_CANCEL = 1

def main():
	global synth, srvHandle
	sc=sdk.EmbeddedSpeechConfig()
	sc.disable_telemetry()
	sc.set_property_by_name("EmbeddedSpeech-DisableTelemetry", "true")
	voicepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'voices')
	for f in os.listdir(voicepath):
		sc.add_path(os.path.join(voicepath, f))
	sc.set_tts_key("ZCjZ7nHDSLvf4gpELteM4AnzaWUjTpn7UkV7D@vvksl0w1SNgon6d1905WANbktDc9S39oaA4r29HJNayXvTq8fJsq")
	sc.set_tts_voice("Microsoft Guy (Natural) - English (United States)")
	sc.set_speech_synthesis_output_format(SpeechSynthesisOutputFormat(16))
	cb = Callbacks()
	stream = PushAudioOutputStream(cb)
	ac = AudioOutputConfig(stream=stream)
	t1 = time.time()
	synth=sdk.SpeechSynthesizer(sc, ac)
	logging.info(f"synth created in {time.time()-t1}")
	voices = []
	for v in synth.get_voices_async().get().voices:
		voices.append({"name": v.name, "locale": v.locale, "short": v.short_name})
	synth.synthesis_started.connect(synthesis_started)
	synth.synthesis_canceled.connect(synthesis_canceled)
	synth.synthesis_completed.connect(synthesis_completed)
	synth.bookmark_reached.connect(bookmark_reached)

	thread = threading.Thread(target=read_stdin)
	thread.daemon = True
	thread.start()
	while True:
		if server_exit:
			break
		# Pipe
		srvHandle = ctypes.windll.kernel32.CreateNamedPipeW(r"\\.\pipe\neural",
		0x03|FILE_FLAG_OVERLAPPED, 0x04|0x02, 1, 64000, 64000, 0, None)
		if srvHandle <= 0:
			raise RuntimeError(f"Can't create server pipe: GetLastError={ctypes.windll.kernel32.GetLastError()}")
		e = ctypes.windll.kernel32.CreateEventW(None, True, False, "neuralSrv")
		ctypes.windll.kernel32.SetEvent(e)
		logging.info("Waiting for connection")
		event = CreateEvent(None, True, False, None)
		o = OVERLAPPED()
		o.hEvent = event
		nWritten = ctypes.c_ulong()
		res = ctypes.windll.kernel32.ConnectNamedPipe(srvHandle, byref(o))
		if res == 0 and ctypes.windll.kernel32.GetLastError() == ERROR_IO_PENDING:
			res = GetOverlappedResult(srvHandle, byref(o), byref(nWritten), True)
		if res == 0 and ctypes.windll.kernel32.GetLastError() == ERROR_PIPE_CONNECTED:
			pass
		elif res == 0:
			logging.info("cnp failed", ctypes.windll.kernel32.GetLastError())
			return
		write_message(MSG_VOICES.to_bytes() + json.dumps(voices).encode('utf-8'))
		handle_messages(srvHandle)
		ctypes.windll.kernel32.CloseHandle(srvHandle)

# The SDK logs exceptions to a diagnostic log with no way to access it, and ignores the stack trace.
# Print them before they get there. Each callback should use this decorator.
def print_exceptions(f):
	def inner(*args, **kwargs):
		try:
			return f(*args, **kwargs)
		except BaseException as e:
			import traceback
			print(traceback.format_exc())
	return inner

def handle_messages(srvHandle):
	while True:
		msg = rp(srvHandle)
		if not msg:
			logging.info("eof")
			return
		if msg[0] == MSG_SPEAK:
			data = msg[1:].decode('utf-8')
			r = synth.speak_ssml_async(data)
		elif msg[0] == MSG_CANCEL:
			synth.stop_speaking_async().get()

buf = ctypes.create_string_buffer(64000)
nRead = ctypes.c_ulong()
def rp(handle):
	data = b''
	event = CreateEvent(None, True, False, None)
	o = OVERLAPPED()
	o.hEvent = event
	while True:
		res = ctypes.windll.kernel32.ReadFile(handle, byref(buf), 8192, byref(nRead), byref(o))
		if res == 0 and ctypes.windll.kernel32.GetLastError() == ERROR_IO_PENDING:
			res = GetOverlappedResult(handle, byref(o), byref(nRead), True)
		elif res == 0 and ctypes.windll.kernel32.GetLastError() == 109:
			ctypes.windll.kernel32.CloseHandle(event)
			return b''
		elif res == 0:
			raise RuntimeError(f"res 0 l {ctypes.windll.kernel32.GetLastError()}")
		if res == 1 and ctypes.windll.kernel32.GetLastError() == ERROR_MORE_DATA:
			data = data + ctypes.string_at(buf, nRead.value)
			continue
		elif res == 1:
			data = data + ctypes.string_at(buf, nRead.value)
			break
		elif res == 0 and ctypes.windll.kernel32.GetLastError() == 109: # EOF
			break
		else:
			raise RuntimeError(f"res {res} l {ctypes.windll.kernel32.GetLastError()}")
	ctypes.windll.kernel32.CloseHandle(event)
	return data

total_ms = 0
class Callbacks(PushAudioOutputStreamCallback):
	def write(self, buffer):
		b = bytes(buffer)
		b = MSG_AUDIO.to_bytes() + b
		write_message(b)
		return len(b)

def write_message(b):
	event = CreateEvent(None, True, False, None)
	o = OVERLAPPED()
	o.hEvent = event
	nWritten = ctypes.c_ulong()
	res = ctypes.windll.kernel32.WriteFile(srvHandle, b, len(b), None, byref(o))
	if res == 0 and ctypes.windll.kernel32.GetLastError() == ERROR_IO_PENDING:
		res = GetOverlappedResult(srvHandle, byref(o), byref(nWritten), True)

@print_exceptions
def synthesis_started(ev):
	write_message(MSG_SPEECH_STARTED.to_bytes() + ev.result.result_id.encode('utf-8'))

@print_exceptions
def synthesis_canceled(ev):
	pass

@print_exceptions
def synthesis_completed(ev):
	write_message(MSG_SPEECH_COMPLETED.to_bytes())

@print_exceptions
def bookmark_reached(event):
	write_message(MSG_MARK.to_bytes() + event.text.encode('utf-8'))

def read_stdin():
	global server_exit
	while True:
		r = sys.stdin.read()
		if not r:
			server_exit = True
			ctypes.windll.kernel32.CancelIoEx(srvHandle, None)
			sys.exit(0)

try:
	main()
except:
	logging.exception("Running main")
