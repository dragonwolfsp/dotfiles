import os
import appModuleHandler
import tones
import ui
import api
from scriptHandler import script
import keyboardHandler

from .lbl.reaper import base, label
from .lbl.reaper.overlay import LBLCheckBox
from .lbl.steevenslatedrummer5.main import SteevenSlateDrummer
from .lbl.gtune.gtune import GTune
from .lbl.kontakt.kontakt import Kontakt
from .lbl.kontakt7.kontakt7 import Kontakt7
from .lbl.surge.surge import Surge
from .lbl.content_missing.main import ContentMissing
from .lbl.sforzando.sforzando import Sforzando
from .lbl.sessiondrummer.sessiondrummer import SessionDrummer


# Import des modules Sibiac
from NVDAObjects.window import Window
from NVDAObjects.IAccessible import IAccessible
import speech
from logHandler import log
import eventHandler
import time
import queueHandler
import core
import oleacc
import controlTypes
import winUser
import api
import ctypes
from . import sibiac
from .sibiac import MoveFocusTo, SIBI, SIBINVDA, XY, Box, TextBox, TextOutBox, ScrollV, Color2Tuple, ColorMatcherObj, ColorMatcher, FindInXRight, FindInYDown, FindRow, FindVRange, FindHRange, chooseKnownOverlay, MouseSlowLeftClick, MouseScroll, FindNearestColor, Control, VList, YRange, YBar, Container, Label, ScrollLabel, PopupLabel, PushBtn, SwitchBtn, FixedTab, FixedTabControl, Combo, Dialog, OpenBtn, PopupMenuButton, Clickable, OptionTable, Pt, FIXED, MOVE, PROPORTIONAL, gSIBI
from .sibiac import SpinLabel
from .sibiac.ezdrummer import EZDrummer
from .sibiac.ni import GuitarRig5
from .sibiac.xln import AD2, AK
from .sibiac.zampler import Zampler
from .sibiac.vsco2 import VSCO2
from .sibiac.igniteampsnadir import IgniteAmpsNadIR
from .sibiac.ezmix import EZMix
from .sibiac.stlthb import SHB

class AppModule(appModuleHandler.AppModule):
    last_fx_selected = ""

    def event_gainFocus(self, obj, nextHandler):
        label.setLabels(obj)
        nextHandler()
   
    @script(gesture="kb:F6")
    def script_select_next_fx(self, gesture):
        if base.isFXWindow() is True:
            self.last_fx_selected = api.getFocusObject().name
            keyboardHandler.KeyboardInputGesture.fromName("F6").send()
        else:
            keyboardHandler.KeyboardInputGesture.fromName("F6").send()


    def chooseNVDAObjectOverlayClasses(self, obj, clsList):
        if obj.windowControlID == 1426:
            clsList.insert(0, LBLCheckBox)
        elif obj.windowClassName.startswith("Plugin") and ("sforzando" in self.last_fx_selected or "DrumAccess" in self.last_fx_selected):
            clsList.insert(0, Sforzando)
        elif obj.windowClassName.startswith("Plugin") and "EZdrummer" in self.last_fx_selected:
            clsList.insert(0, EZDrummer)
        elif obj.windowClassName.startswith("GWin") and "GTune" in self.last_fx_selected:
            clsList.insert(0, GTune)
        elif (obj.windowClassName.startswith("reaperPlug") or obj.windowClassName.startswith("Opt")) and "Kontakt 7" in self.last_fx_selected:
            clsList.insert(0, Kontakt7)
        elif (obj.windowClassName.startswith("NI") or obj.windowClassName.startswith("Opt")) and "Kontakt" in self.last_fx_selected:
            clsList.insert(0, Kontakt)
        elif obj.windowClassName.startswith('NIVSTChildWindow') and "Guitar Rig" in self.last_fx_selected:
            clsList.insert(0, GuitarRig5)
        elif obj.windowClassName.startswith('Plugin') and "Zampler" in self.last_fx_selected:
            clsList.insert(0, Zampler)
        elif obj.windowClassName.startswith('JUCE') and "VSCO2" in self.last_fx_selected:
            clsList.insert(0, VSCO2)
        elif obj.windowClassName.startswith('JUCE') and "Addictive Drums" in self.last_fx_selected:
            clsList.insert(0, AD2)
        elif obj.windowClassName.startswith('JUCE') and "Addictive Keys" in self.last_fx_selected:
            clsList.insert(0, AK)
        elif obj.windowClassName.startswith('VSTGUI') and "NadIR" in self.last_fx_selected:
            clsList.insert(0, IgniteAmpsNadIR)
        elif obj.windowClassName.startswith('Plugin') and "EZmix" in self.last_fx_selected:
            clsList.insert(0, EZMix)
        elif "Surge" in self.last_fx_selected and obj.name == 'Window':
            clsList.insert(0, Surge)
        elif obj.windowClassName.startswith('JUCE') and "STL Tonality" in self.last_fx_selected:
            clsList.insert(0, SHB)
        elif obj.windowClassName.startswith("JUCE") and "SSDSampler" in self.last_fx_selected:
            clsList.insert(0, SteevenSlateDrummer)
        elif obj.name == "Content Missing":
            clsList.insert(0, ContentMissing)
        elif obj.windowClassName.startswith('PAL') and "SessionDrummer" in base.getSelectedFXName():
            clsList.insert(0, SessionDrummer)
