# Import des modules NVDA
import ui
import api
import keyboardHandler
import config
from NVDAObjects.IAccessible import IAccessible
from scriptHandler import script

# Import des modules LBL
from ..api.navobject import NavObject
from ..api.ocr import LBLOCR
from ..api.mouse import Mouse
from ..api import machine

class ContentMissing(IAccessible):
    name = "Content Missing, To browse your computer to locate the folder for this library, press Space for Kontakt 6, and Enter for Kontakt 7."
    mouse = Mouse()

    @script(gesture="kb:Space")
    def script_Kontakt6_BrowseForFolder(self, gesture):
        self.mouse.moveAndLeftClick(224, 243)

    @script(gesture="kb:Enter")
    def script_Kontakt7_BrowseForFolder(self, gesture):
        if machine.get_machine_type() == "laptop":
            self.mouse.moveAndLeftClick(275, 420)
        elif machine.get_machine_type() == "desktop":
            self.mouse.moveAndLeftClick(220, 336)

    
    @script(gestures=["kb:Tab", "kb:Shift+Tab"])
    def script_SayHelpMessage(self, gesture):
        ui.message("To browse your computer to locate the folder for this library, press Space for Kontakt 6, and Enter for Kontakt 7.")
