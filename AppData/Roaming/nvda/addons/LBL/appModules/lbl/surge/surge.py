import time

# Import des modules NVDA
import ui
from NVDAObjects.IAccessible import IAccessible
from scriptHandler import script

# Import des modules LBL
from ..api.navobject import NavObject
from ..api.ocr import LBLOCR
from ..api.mouse import Mouse

class Surge(IAccessible):
    name = "LBL_SurgeSynth"
    mouse = Mouse()
        
    @script(gesture="kb:uparrow")
    def script_goToPreviousCategory(self, gesture):
        self.mouse.moveAndLeftClick(166, 47)
        time.sleep(0.2)
        ui.message(LBLOCR.getText([195, 14, 296, 30]))

    @script(gesture="kb:downarrow")
    def script_goToNextCategory(self, gesture):
        self.mouse.moveAndLeftClick(179, 47)
        time.sleep(0.2)
        ui.message(LBLOCR.getText([195, 14, 296, 30]))

    @script(gesture="kb:leftarrow")
    def script_goToPreviousPatch(self, gesture):
        self.mouse.moveAndLeftClick(252, 46)
        time.sleep(0.3)
        ui.message(LBLOCR.getText([293, 20, 432, 30]))

    @script(gesture="kb:rightarrow")
    def script_goToNextPatch(self, gesture):
        self.mouse.moveAndLeftClick(267, 46)
        time.sleep(0.3)
        ui.message(LBLOCR.getText([293, 20, 432, 30]))
