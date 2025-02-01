# Import des modules NVDA
import ui
from NVDAObjects.IAccessible import IAccessible
from scriptHandler import script

# Import des modules LBL
from ..api.navobject import NavObject
from ..api.ocr import LBLOCR
from ..api.mouse import Mouse
from .zones import controlZone
from ..api import machine


class Sforzando(IAccessible):
    name = "LBL_Sforzando"
    controlZone = NavObject(controlZone, 0)
    mouse = Mouse()

    @script(gesture="kb:enter")
    def script_click_on_menu(self, gesture):
        ui.message(self.controlZone.getObject(mouse = "move_and_click")["name"])

    @script(gesture="kb:tab")
    def script_goToPreviousZone(self, gesture):
        ui.message(self.controlZone.getPreviousObject(mouse = "move")["name"])

    @script(gesture="kb:shift+tab")
    def script_goToNextZone(self, gesture):
        ui.message(self.controlZone.getNextObject(mouse = "move")["name"])

    @script(gestures=["kb:uparrow", "kb:downarrow", "kb:leftarrow", "kb:rightarrow"])
    def script_arros_cancelation(self, gesture):
        pass

    @script(gesture="kb:m")
    def script_get_machine_type(self, gesture):
        if machine.get_machine_type() == "laptop":
            ui.message("Laptop")
        elif machine.get_machine_type() == "desktop":
            ui.message("Desktop")

    @script(gesture="kb:i")
    def script_say_instrument_name(self, gesture):
        if machine.get_machine_type() == "laptop":
            instrument = LBLOCR.getText([112, 20, 295, 50])
        elif machine.get_machine_type() == "desktop":
            instrument = LBLOCR.getText([112, 20, 295, 50])

        instrument = instrument.lower()\
        .replace('beii', 'bell')\
        .replace('beil', 'bell')\
        .replace('beli', 'bell')\
        .replace('ciap', 'clap')\
        .replace('roiand', 'roland')\
        .replace('cymbai', 'cymbal')\
        .replace('spiash', 'splash')\
        .replace('timbaie', 'timbale')\
        .replace('|', 'l')\
        .replace('\n', '')
        
        
        ui.message(instrument )
