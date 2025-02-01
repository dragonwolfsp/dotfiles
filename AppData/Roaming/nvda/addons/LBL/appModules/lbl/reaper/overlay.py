import keyboardHandler
import api
import ui
import config

from NVDAObjects.IAccessible import IAccessible
from scriptHandler import script
from . import base

class LBLCheckBox(IAccessible):
    @script(gesture="kb:tab")
    def script_goToFX(self, gesture):
        obj = api.getFocusObject()
        fxName = base.getSmartName()

        if fxName:
            obj = obj.parent.next.firstChild
            api.setFocusObject(obj)
            ui.message(fxName)
            config.conf["mouse"]["enableMouseTracking"] = False
        else:
            keyboardHandler.KeyboardInputGesture.fromName("tab").send()
