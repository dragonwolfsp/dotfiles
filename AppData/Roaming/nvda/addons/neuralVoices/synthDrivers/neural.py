from synthDriverHandler import SynthDriver, synthDoneSpeaking, synthIndexReached, VoiceInfo
import os
import speechXml
from speech.commands import IndexCommand, RateCommand, PitchCommand, VolumeCommand
import nvwave
import threading
import winKernel
import languageHandler
import ctypes
from ctypes import byref
import subprocess
import config
from typing import Set, Any, Generator
from speech import SpeechSequence
from serial.win32 import FILE_FLAG_OVERLAPPED, OVERLAPPED, LPOVERLAPPED, CreateEvent, ERROR_IO_PENDING, GetOverlappedResult
import json

ERROR_MORE_DATA = 234
MSG_SPEECH_STARTED = 1
MSG_AUDIO = 2
MSG_MARK = 3
MSG_SPEECH_COMPLETED = 4
MSG_VOICES = 5
#C2S
MSG_SPEAK = 0
MSG_CANCEL = 1

class SynthDriver(SynthDriver):
	MIN_RATE = 50
	MAX_RATE = 250
	MIN_PITCH = 50
	MAX_PITCH = 250
	name = "neural"
	description = "Neural Voices"
	supportedCommands = {
		IndexCommand,
		PitchCommand,
		}
	supportedNotifications = {synthIndexReached, synthDoneSpeaking}
	supportedSettings = (
	SynthDriver.VoiceSetting(),
	SynthDriver.RateSetting(),
	SynthDriver.PitchSetting(),
	)

	@classmethod
	def check(cls):
		return True

	def __init__(self):
		super().__init__()
		server_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'server', 'server.exe')
		if os.path.exists(server_path):
			self.proc = subprocess.Popen(server_path, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
		else:
			self.proc = None
		e = ctypes.windll.kernel32.CreateEventW(None, True, False, "neuralSrv")
		res = ctypes.windll.kernel32.WaitForSingleObject(e, 5000)
		winKernel.closeHandle(e)
		if res != 0:
			if self.proc:
				self.proc.stdin.close()
			raise RuntimeError(f"Event not signaled: {ctypes.windll.kernel32.GetLastError()}")
		self.pipe = ctypes.windll.kernel32.CreateFileW(r"\\.\pipe\neural",
		winKernel.GENERIC_READ|winKernel.GENERIC_WRITE, 0, None, winKernel.OPEN_EXISTING, FILE_FLAG_OVERLAPPED, None)
		if self.pipe == -1:
			raise RuntimeError(ctypes.windll.kernel32.GetLastError())
		t = ctypes.c_long(2)
		res = ctypes.windll.kernel32.SetNamedPipeHandleState(self.pipe, byref(t), 0, 0)
		if res != 1:
			raise RuntimeError(res)
		self.player = nvwave.WavePlayer(samplesPerSec=24000, channels=1, bitsPerSample=16, outputDevice=config.conf["speech"]["outputDevice"])
		# Set initial rate
		self._rate = 100
		self._pitch = 100
		self.is_processing = False
		self.current_speech_id = None
		self.voice_event = threading.Event()
		self.voice_data = None
		self.rt = threading.Thread(target=self.readerThread)
		self.rt.daemon = True
		self.rt.start()
		self.queue = []
		if not self.voice_event.wait(5):
			raise RuntimeError("Voice list not received within timeout")
		self.voice = self.get_default_voice()
		self.was_canceled = False

	def speak(self, speechSequence):
		self.was_canceled = False
		converter = Converter('en-US', ['en-US'], self._rate, self._pitch, 100, self._voice)
		s = converter.convertToXml(speechSequence)
		self.queue.append(s)
		if not self.is_processing:
			self._processQueue()

	def _processQueue(self):
		while self.queue:
			item = self.queue.pop(0)
			self.is_processing = True
			self.was_canceled = False
			header = b'\x00'
			self.write_message(header + item.encode('utf-8'))
			self.is_processing = False
			return
		self.is_processing = False

	def cancel(self):
		self.queue = []
		self.write_message(MSG_CANCEL.to_bytes())
		self.current_speech_id = None
		self.player.stop()
		self.was_canceled = True

	def _get_rate(self):
		return self._paramToPercent(self._rate, self.MIN_RATE, self.MAX_RATE)
	def _set_rate(self, v):
		self._rate = self._percentToParam(v, self.MIN_RATE, self.MAX_RATE)

	def _get_pitch(self):
		return self._paramToPercent(self._pitch, self.MIN_PITCH, self.MAX_PITCH)
	def _set_pitch(self, v):
		self._pitch = self._percentToParam(v, self.MIN_PITCH, self.MAX_PITCH)

	def synthesis_completed(self):
		synthDoneSpeaking.notify(synth=self)
		self._processQueue()

	def write_message(self, data):
		event = CreateEvent(None, True, False, None)
		o = OVERLAPPED()
		o.hEvent = event
		nWritten = ctypes.c_long()
		res = ctypes.windll.kernel32.WriteFile(self.pipe, data, len(data), None, byref(o))
		if res == 0 and ctypes.windll.kernel32.GetLastError() == ERROR_IO_PENDING:
			res = winKernel.waitForSingleObject(event, INFINITE)
		ctypes.windll.kernel32.CloseHandle(event)
		return res

	def readerThread(self):
		while True:
			msg = rp(self.pipe)
			if not msg:
				return
			elif msg[0] == MSG_SPEECH_STARTED:
				if self.was_canceled:
					continue
				self.current_speech_id = msg[1:]
			elif msg[0] == MSG_AUDIO:
				if self.current_speech_id is None:
					continue
				self.player.feed(msg[1:])
			elif msg[0] == MSG_MARK:
				data = msg[1:].decode('utf-8')
				synthIndexReached.notify(synth=self, index=int(data))
			elif msg[0] == MSG_SPEECH_COMPLETED:
				synthDoneSpeaking.notify(synth=self)
				self.player.idle()
				self._processQueue()
			elif msg[0] == MSG_VOICES:
				self.voice_data = json.loads(msg[1:].decode('utf-8'))
				self.voice_event.set()

	def terminate(self):
		if self.pipe is not None:
			ctypes.windll.kernel32.CloseHandle(self.pipe)
			self.pipe = None
		if self.proc is not None:
			self.proc.stdin.close()
			try:
				self.proc.wait(timeout=1)
			except subprocess.TimeoutExpired:
				self.proc.kill()

	def _getAvailableVoices(self):
		voices = {}
		for v in self.voice_data:
			info = VoiceInfo(v['name'], v['name'], language=v['locale'])
			voices[v['name']] = info
		return voices

	def _set_voice(self, v):
		if v in self._getAvailableVoices():
			self._voice = v
			return
		raise LookupError(f"Unknown voice: {v}")

	def _get_voice(self):
		return self._voice

	def get_default_voice(self):
		voices = self._getAvailableVoices()
		fullWindowsLanguage = languageHandler.getWindowsLanguage()
		baseWindowsLanguage = fullWindowsLanguage.split('_')[0]
		NVDALanguage = languageHandler.getLanguage()
		if NVDALanguage.startswith(baseWindowsLanguage):
			# add country information if it matches
			NVDALanguage = fullWindowsLanguage
		# Try matching to the NVDA language
		for voice in voices.values():
			if voice.language.startswith(NVDALanguage):
				return voice.id
		# Try matching to the system language and country
		if fullWindowsLanguage != NVDALanguage:
			for voice in voices.values():
				if voice.language == fullWindowsLanguage:
					return voice.id
		# Try matching to the system language
		if baseWindowsLanguage not in {fullWindowsLanguage, NVDALanguage}:
			for voice in voices.values():
				if voice.language.startswith(baseWindowsLanguage):
					return voice.id
		for voice in voices.values():
			return voice.id
		raise VoiceUnsupportedError("No voices available")

	def pause(self, switch):
		self.player.pause(switch)

# I don't actually understand how this class is supposed to work.
class Converter(speechXml.SsmlConverter):

	def __init__(
			self,
			defaultLanguage: str,
			availableLanguages: Set[str],
			rate: float,
			pitch: float,
			volume: float,
			voice: str,
	):
		"""
		Used for older OneCore installations (OneCore API < 5),
		where supportsProsodyOptions is False.
		This means we must initially set a good default for rate, volume and pitch,
		as this can't be changed after initialization.

		@param defaultLanguage: language with locale, installed by OneCore (e.g. 'en_US')
		@param availableLanguages: languages with locale, installed by OneCore (e.g. 'zh_HK', 'en_US')
		@param rate: from 0-100
		@param pitch: from 0-100
		@param volume: from 0-100
		"""
		super().__init__(defaultLanguage)
		self._rate = rate
		self._pitch = pitch
		self._volume = volume
		self._voice = voice

	def generateBalancerCommands(self, speechSequence: SpeechSequence) -> Generator[Any, None, None]:
		commands = super().generateBalancerCommands(speechSequence)
		# The EncloseAllCommand from SSML must be first.
		yield next(commands)
		yield speechXml.SetAttrCommand("voice", "name", self._voice)
		# OneCore didn't provide a way to set base prosody values before API version 5.
		# Therefore, the base values need to be set using SSML.
		yield self.convertRateCommand(RateCommand(multiplier=1))
		yield self.convertVolumeCommand(VolumeCommand(multiplier=1))
		yield self.convertPitchCommand(PitchCommand(multiplier=1))
		for command in commands:
			yield command

	def convertRateCommand(self, command):
		return self._convertProsody(command, "rate", 50, self._rate)

	def convertPitchCommand(self, command):
		return self._convertProsody(command, "pitch", 100, self._pitch)

	def convertVolumeCommand(self, command):
		return self._convertProsody(command, "volume", 100, self._volume)

	def _convertProsody(self, command, attr, default, base=None):
		if base is None:
			base = default
		if command.multiplier == 1 and base == default:
			# Returning to synth default.
			return speechXml.DelAttrCommand("prosody", attr)
		else:
			# Multiplication isn't supported, only addition/subtraction.
			# The final value must therefore be relative to the synthesizer's default.
			val = base * command.multiplier - default
			return speechXml.SetAttrCommand("prosody", attr, "%d%%" % val)

# Read a message from a pipe
buf = ctypes.create_string_buffer(64000)
nRead = ctypes.c_ulong()
def rp(handle):
	data = b''
	while True:
		event = CreateEvent(None, True, False, None)
		o = OVERLAPPED()
		o.hEvent = event
		res = ctypes.windll.kernel32.ReadFile(handle, byref(buf), 8192, None, byref(o))
		e = ctypes.windll.kernel32.GetLastError()
		if res == 0 and ctypes.windll.kernel32.GetLastError() == ERROR_IO_PENDING:
			res = GetOverlappedResult(handle, byref(o), byref(nRead), True)
		if res == 0 and ctypes.windll.kernel32.GetLastError() == 109:
			ctypes.windll.kernel32.CloseHandle(event)
			return b''
		elif res == 0 and ctypes.windll.kernel32.GetLastError() == ERROR_MORE_DATA:
			res = GetOverlappedResult(handle, byref(o), byref(nRead), True)
			data = data + ctypes.string_at(buf, nRead.value)
			ctypes.windll.kernel32.ResetEvent(event)
			continue
		elif res == 0:
			raise RuntimeError(f"res 0 l {ctypes.windll.kernel32.GetLastError()}")
		if res == 1:
			res = GetOverlappedResult(handle, byref(o), byref(nRead), True)
			data = data + ctypes.string_at(buf, nRead.value)
			break
		elif res == 0 and ctypes.windll.kernel32.GetLastError() == 109: # EOF
			break
		else:
			raise RuntimeError(f"res {res} l {ctypes.windll.kernel32.GetLastError()}")
	ctypes.windll.kernel32.CloseHandle(event)
	return data
