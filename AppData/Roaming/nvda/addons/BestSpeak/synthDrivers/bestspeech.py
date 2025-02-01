# synthDrivers\bestspeech.py
#
# Revised version with a request queue and robust error handling:
# - Uses a ThreadPoolExecutor as an instance attribute.
# - Re-init the engine from scratch before every chunk.
# - Shut down and unload the DLL after each chunk in _speakBg().
# - Number Processing, Abbreviations inverted, Phrase Prediction logic remain, Nasality.
# - Introduce a request queue so if you move too quickly, chunks are queued, not lost.
# - When current chunk finishes, next chunk is processed from the queue.
# - Add robust error handling in _processNextChunk() and _speakBg() to prevent the queue-processing thread from crashing.
# - Code clean-up
import os
from synthDriverHandler import SynthDriver, synthIndexReached, synthDoneSpeaking
import ctypes
from ctypes import POINTER, c_long, c_char_p, c_int, byref, wintypes
from windowUtils import CustomWindow
import winUser
from speech.commands import IndexCommand, PitchCommand, CharacterModeCommand
import threading
from concurrent.futures import ThreadPoolExecutor
from autoSettingsUtils.driverSetting import DriverSetting, BooleanDriverSetting
from autoSettingsUtils.utils import StringParameterInfo
from logHandler import log
import re

RATE_MIN = 100
RATE_MAX = -100
PITCH_MIN = 43
PITCH_MAX = 250
INFLECTION_MIN = -80
INFLECTION_MAX = 100
VOLUME_MIN = -40
VOLUME_MAX = 5
NASALITY_MIN = -70
NASALITY_MAX = 20

ttsLock = threading.Lock()

def clampFreq(freq):
    return max(45, min(freq,600))

class Window(CustomWindow):
    className = 'NVDABestspeech'

    def __init__(self, *args, synth=None, **kwargs):
        self.synth = synth
        super().__init__(*args, **kwargs)

    def windowProc(self, hwnd, msg, wParam, lParam):
        if msg == 957:  # TTS_BUFFER_FULL
            if self.synth and self.synth.handle and self.synth.bstRelBuf:
                try:
                    self.synth.bstRelBuf(self.synth.handle)
                except OSError:
                    log.error("Error calling bstRelBuf", exc_info=True)
        elif msg == 1235:  # Shut up requested
            if self.synth and self.synth.handle and self.synth.bstShutup:
                try:
                    self.synth.bstShutup(self.synth.handle)
                    self.synth._canceled = True
                    with self.synth._requestLock:
                        self.synth._requestQueue.clear()
                except OSError:
                    log.error("Error calling bstShutup in windowProc", exc_info=True)
        return None

class SynthDriver(SynthDriver):
    name = 'bestspeech'
    description = 'Bestspeech'
    supportedSettings = (
        SynthDriver.RateSetting(),
        SynthDriver.PitchSetting(),
        SynthDriver.InflectionSetting(),
        SynthDriver.VolumeSetting(),
        DriverSetting("headsize", "&Headsize", defaultVal="0", availableInSettingsRing=True),
        DriverSetting("excitation", "&Excitation", defaultVal="0", availableInSettingsRing=True),
        DriverSetting("nasality", "&Nasality", defaultVal="65", availableInSettingsRing=True),
        BooleanDriverSetting("numberProcessing", "&Number Processing", defaultVal=False),
        BooleanDriverSetting("abbreviations", "&Abbreviations", defaultVal=True),
        BooleanDriverSetting("phrase_prediction", "&Phrase Prediction", defaultVal=True)
    )
    supportedNotifications = {synthIndexReached, synthDoneSpeaking}
    supportedCommands = {PitchCommand, CharacterModeCommand, IndexCommand}

    _headsizes = {
        "0": StringParameterInfo("0", "0"),
        "1": StringParameterInfo("1", "1"),
        "2": StringParameterInfo("2", "2"),
        "3": StringParameterInfo("3", "3"),
        "4": StringParameterInfo("4", "4"),
        "5": StringParameterInfo("5", "5"),
        "6": StringParameterInfo("6", "6")
    }

    _excitations = {
        "0": StringParameterInfo("0", "0"),
        "1": StringParameterInfo("1", "1"),
        "2": StringParameterInfo("2", "2"),
        "3": StringParameterInfo("3", "3"),
        "4": StringParameterInfo("4", "4"),
        "5": StringParameterInfo("5", "5"),
        "6": StringParameterInfo("6", "6")
    }

    _nasalitys = {
        "0": StringParameterInfo("0","0"),
        "5": StringParameterInfo("5","5"),
        "10": StringParameterInfo("10","10"),
        "15": StringParameterInfo("15","15"),
        "20": StringParameterInfo("20","20"),
        "25": StringParameterInfo("25","25"),
        "30": StringParameterInfo("30","30"),
        "35": StringParameterInfo("35","35"),
        "40": StringParameterInfo("40", "40"),
        "45": StringParameterInfo("45","45"),
        "50": StringParameterInfo("50", "50"),
        "55": StringParameterInfo("55","55"),
        "60": StringParameterInfo("60", "60"),
        "65": StringParameterInfo("65","65"),
        "70": StringParameterInfo("70","70"),
        "75": StringParameterInfo("75","75"),
        "80": StringParameterInfo("80", "80"),
        "85": StringParameterInfo("85","85"),
        "90": StringParameterInfo("90","90"),
        "95": StringParameterInfo("95","95"),
        "100": StringParameterInfo("100","100")
    }

    @classmethod
    def check(cls):
        return True

    def __init__(self):
        super().__init__()
        log.info("Initializing bestspeech with minimal changes...")

        self.executor = ThreadPoolExecutor(max_workers=1)

        self._rate = 50
        self._pitch = 15
        self._inflection = 60
        self._volume = 90
        self._headsize = "0"
        self._excitation = "0"
        self._nasality = "75"
        self._canceled = False

        self.win = Window(synth=self)
        self.table = str.maketrans("’", "'")
        self.dll = None
        self.handle = None
        self._numberProcessing = False
        self._abbreviations = True
        self._phrase_prediction = True

        self._requestQueue = []
        self._requestLock = threading.Lock()
        self._reading = False

        self._initEngine()

    def _initEngine(self):
        self._closeEngine()
        dll_path = os.path.join(os.path.dirname(__file__), 'b32_tts.dll')
        self.dll = ctypes.CDLL(dll_path)

        self.dll.bstCreate.argtypes = [ctypes.POINTER(POINTER(c_long))]
        self.dll.bstCreate.restype = c_int
        self.dll.TtsWav.argtypes = [POINTER(c_long), wintypes.HWND, c_char_p]
        self.dll.TtsWav.restype = c_int
        self.dll.bstRelBuf.argtypes = [POINTER(c_long)]
        self.dll.bstRelBuf.restype = None
        self.bstRelBuf = self.dll.bstRelBuf

        _bstShutup = getattr(self.dll, "bstShutup", None)
        if _bstShutup:
            _bstShutup.restype = None
            _bstShutup.argtypes = [POINTER(c_long)]
        self.bstShutup = _bstShutup

        _bstClose = getattr(self.dll, "bstClose", None)
        if _bstClose:
            _bstClose.argtypes = [POINTER(c_long)]
            _bstClose.restype = None
        self.bstClose = _bstClose

        self.dll.bstDestroy.argtypes = [POINTER(c_long)]
        self.dll.bstDestroy.restype = None
        self.bstDestroy = self.dll.bstDestroy

        handle_ptr = POINTER(c_long)()
        res = self.dll.bstCreate(byref(handle_ptr))
        if res != 0 or not handle_ptr:
            raise RuntimeError("Failed to create TTS handle")
        self.handle = handle_ptr

    def _closeEngine(self):
        if self.handle:
            try:
                if self.bstShutup:
                    self.bstShutup(self.handle)
                if self.bstClose:
                    self.bstClose(self.handle)
                self.bstDestroy(self.handle)
                self.handle = None
            except OSError:
                pass
        if self.dll:
            ctypes.windll.kernel32.FreeLibrary(self.dll._handle)
            self.dll = None

    def terminate(self):
        self.cancel()
        self.executor.shutdown(wait=True)
        self._closeEngine()
        if self.win:
            self.win.destroy()
            self.win = None

    def cancel(self):
        self._canceled = True
        if self.handle and self.bstShutup:
            try:
                self.bstShutup(self.handle)
            except OSError:
                pass
        with self._requestLock:
            self._requestQueue.clear()

    def speak(self, speechSequence):
        if not self.handle:
            self._initEngine()
            if not self.handle:
                synthDoneSpeaking.notify(synth=self)
                return

        self._canceled = False
        tts_rate = self._percentToParam(self._rate, RATE_MIN, RATE_MAX)
        tts_pitch = self._percentToParam(self._pitch, PITCH_MIN, PITCH_MAX)
        tts_h = self._percentToParam(self._inflection, INFLECTION_MIN, INFLECTION_MAX)
        tts_g = self._percentToParam(self._volume, VOLUME_MIN, VOLUME_MAX)
        tts_hs = self._headsize
        tts_e = self._excitation
        nasality_int = int(self._nasality)
        tts_u = self._percentToParam(nasality_int, NASALITY_MIN, NASALITY_MAX)

        phrase_pred_str = "" if self._phrase_prediction else "~~1,1]"
        abbrev_val = "0" if self._abbreviations else "1"
        text_pieces = [
            f"{phrase_pred_str}~r{tts_rate}]~v{tts_hs}]~f{tts_pitch}]~h{tts_h}]~g{tts_g}]~u{tts_u}]~e{tts_e}]~n2,0]~n10,{abbrev_val}]"
        ]
        idx = []
        char_mode_on = False
        pitch_modified = False
        base_freq = tts_pitch

        for item in speechSequence:
            if isinstance(item, str):
                if char_mode_on:
                    text_pieces.append(item)
                    text_pieces.append("~n1,0]")
                    char_mode_on = False
                else:
                    text_pieces.append(item)
                if pitch_modified:
                    text_pieces.append(f"~f{base_freq}]")
                    pitch_modified = False
            elif isinstance(item, IndexCommand):
                idx.append(item.index)
            elif isinstance(item, CharacterModeCommand):
                if item.state:
                    text_pieces.append("~n1,1]")
                    char_mode_on = True
                else:
                    text_pieces.append("~n1,0]")
                    char_mode_on = False
            elif isinstance(item, PitchCommand):
                multiplier = getattr(item, 'multiplier', 1)
                if multiplier == 1:
                    text_pieces.append(f"~f{base_freq}]")
                    pitch_modified = False
                else:
                    new_pitch = clampFreq(int(base_freq * multiplier))
                    text_pieces.append(f"~f{new_pitch}]")
                    pitch_modified = True

        text_pieces.append("~|")
        final_text = " ".join(text_pieces)
        if not final_text.strip():
            synthDoneSpeaking.notify(synth=self)
            return

        if self._numberProcessing:
            final_text = self._formatNumbers(final_text)

        with self._requestLock:
            self._requestQueue.append((final_text, idx))
        if not self._reading:
            self._processNextChunk()

    def _processNextChunk(self):
        with self._requestLock:
            if self._canceled or not self._requestQueue:
                self._reading = False
                return
            final_text, idx = self._requestQueue.pop(0)

        self._reading = True
        self._initEngine()
        try:
            self.executor.submit(self._speakBg, final_text, idx)
        except:
            self._reading = False
            self._processNextChunk()

    def _formatNumbers(self, text):
        def replace_num(m):
            num_str = m.group(0)
            return format(int(num_str), ",")
        return re.sub(r"\b\d{5,}\b", replace_num, text)

    def _speakBg(self, text, idx):
        try:
            if not self.handle:
                synthDoneSpeaking.notify(synth=self)
                self._reading = False
                self._processNextChunk()
                return
            txt = text.translate(self.table).encode('windows-1252', 'replace')
            with ttsLock:
                try:
                    result = self.dll.TtsWav(self.handle, wintypes.HWND(self.win.handle), txt)
                except:
                    pass
                finally:
                    self._closeEngine()
            if not self._canceled:
                for i in idx:
                    synthIndexReached.notify(synth=self, index=i)
            synthDoneSpeaking.notify(synth=self)
        except:
            self._closeEngine()
            synthDoneSpeaking.notify(synth=self)
        finally:
            self._reading = False
            self._processNextChunk()

    def pause(self, switch):
        if switch:
            self.cancel()

    def _get_rate(self):
        return self._rate
    def _set_rate(self, val):
        self._rate = val

    def _get_pitch(self):
        return self._pitch
    def _set_pitch(self, val):
        self._pitch = val

    def _get_inflection(self):
        return self._inflection
    def _set_inflection(self, val):
        self._inflection = val

    def _get_volume(self):
        return self._volume
    def _set_volume(self, val):
        self._volume = val

    def _get_nasality(self):
        return self._nasality
    def _set_nasality(self, val):
        if val in self._nasalitys:
            self._nasality = val
        else:
            self._nasality = "50"

    def _get_availableHeadsizes(self):
        return self._headsizes

    def _get_availableExcitations(self):
        return self._excitations

    def _get_availableNasalitys(self):
        return self._nasalitys

    def _get_headsize(self):
        return self._headsize
    def _set_headsize(self, val):
        if val in self._headsizes:
            self._headsize = val
        else:
            self._headsize = "0"

    def _get_excitation(self):
        return self._excitation
    def _set_excitation(self, val):
        if val in self._excitations:
            self._excitation = val
        else:
            self._excitation = "0"

    def _get_numberProcessing(self):
        return self._numberProcessing
    def _set_numberProcessing(self, val):
        self._numberProcessing = bool(val)

    def _get_abbreviations(self):
        return self._abbreviations
    def _set_abbreviations(self, val):
        self._abbreviations = bool(val)

    def _get_phrase_prediction(self):
        return self._phrase_prediction
    def _set_phrase_prediction(self, val):
        self._phrase_prediction = bool(val)
