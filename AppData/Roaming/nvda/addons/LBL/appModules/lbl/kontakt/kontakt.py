# Import des modules Python
import time, os

# Import des modules NVDA
import ui
import api
import keyboardHandler
from NVDAObjects.IAccessible import IAccessible
from scriptHandler import script

# Import des modules LBL
from ..api.navobject import NavObject
from ..api.ocr import LBLOCR
from ..api.mouse import Mouse
from ..api import screen

# Import des modules propres à Kontakt
from .zones import kontaktZone
from .tabs import kontaktTabs

img_dir = os.path.dirname(__file__)
disc_button_path = os.path.join(img_dir, "images", "disc_button.png")
load_button_path = os.path.join(img_dir, "images", "load_button.png")
library_tab_path = os.path.join(img_dir, "images", "library_tab.png")
manage_library_path = os.path.join(img_dir, "images", "manage_library_button.png")
add_library_button_path = os.path.join(img_dir, "images", "add_library_button.png")
previous_next_instrument_path = os.path.join(img_dir, "images", "previous_next_instrument.png")

class Kontakt(IAccessible):
    name = "LBL_Kontakt"
    zones = NavObject(kontaktZone)
    tabs = NavObject(kontaktTabs)
    mouse = Mouse()
    mode = "Default"

    @script(gesture="kb:enter")
    def script_defaultAction(self, gesture):
        if self.zones.getObject()['name'] == 'Load, button':
            instrument = LBLOCR.getText([409, 80, 626, 97])

            if instrument.replace('\n', '') != '':
                ui.message('Instrument already loaded')
            else:
                ui.message('Load Instrument')
                screen.locate_and_click(disc_button_path)
                screen.locate_and_click(load_button_path, xCleanMouse = 150, yCleanMouse = 150)
        elif self.zones.getObject()['name'] == 'Add Library, button':
            ui.message('Add Library')
            screen.locate_and_click(library_tab_path)
            time.sleep(1)
            screen.locate_and_click(manage_library_path)
            time.sleep(1)
            screen.locate_and_click(add_library_button_path)

    @script(gesture="kb:shift+tab")        
    def script_goToPreviousZone(self, gesture):
        ui.message(self.zones.getPreviousObject()['name'])

    @script(gesture="kb:tab")        
    def script_goToNextZone(self, gesture):
        ui.message(self.zones.getNextObject()['name'])

    @script(gesture="kb:i")
    def script_sayInstrumentName(self, gesture):
        instrument = LBLOCR.getText([409, 80, 626, 97])

        if instrument.replace('\n', '') == '':
            ui.message('No instrument')
        else:
            ui.message(instrument)

    @script(gesture="kb:delete")
    def script_closeInstrument(self, gesture):
        instrument = LBLOCR.getText([409, 80, 626, 97])

        if instrument.replace('\n', '') == '':
            ui.message('No instrument')
        else:
            ui.message(LBLOCR.getText([409, 80, 626, 97]))
            ui.message('Closed')
            self.mouse.moveAndLeftClick(956, 81)

    @script(gesture="kb:o")        
    def script_setOmniChanels(self, gesture):
        instrument = LBLOCR.getText([409, 80, 626, 97])

        if instrument.replace('\n', '') == '':
            ui.message('No instrument')
        else:
            self.mouse.moveAndLeftClick(517, 125)
            time.sleep(0.2)
            self.mouse.moveAndLeftClick(493, 139)

    @script(gesture="kb:m")
    def script_sayMidiChanel(self, gesture):
        instrument = LBLOCR.getText([409, 80, 626, 97])

        if instrument.replace('\n', '') == '':
            ui.message('No instrument')
        else:
            ui.message(LBLOCR.getText([402, 118, 499, 131]).replace('\n', '')
            .replace('[', '')
            .replace(']', '')
            .replace('FI', 'A')
            .replace('Chr', 'Chanel : ')
            .replace('Ch:', 'Chanel : '))

    @script(gesture="kb:p")
    def script_previousInstrument(self, gesture):
        instrument = LBLOCR.getText([409, 80, 626, 97])

        if instrument.replace('\n', '') == '':
            ui.message('No instrument')
        else:
            screen.locate_and_click(previous_next_instrument_path, xOffset = -32, xCleanMouse = 150, yCleanMouse = 150)

    @script(gesture="kb:n")
    def script_nextInstrument(self, gesture):
        instrument = LBLOCR.getText([409, 80, 626, 97])

        if instrument.replace('\n', '') == '':
            ui.message('No instrument')
        else:
            screen.locate_and_click(previous_next_instrument_path, xOffset = -16, xCleanMouse = 150, yCleanMouse = 150)

    @script(gestures=["kb:uparrow", "kb:downarrow", "kb:leftarrow", "kb:rightarrow"])
    def script_bypassKeys(self, gesture):
        pass

    @script(gesture="kb:e")
    def script_editInstrument(self, gesture):
        instrument = LBLOCR.getText([409, 80, 626, 97])

        if instrument.replace('\n', '') == '':
            ui.message('No instrument')
        else:
            self.mode = "Edition"

    @script(gesture="kb:NVDA+d")
    def script_debug(self, gesture):
        ui.message(str(self.getXLocation(67.47)))

    def getXLocation(self, pourcent):
        result = pourcent * api.getFocusObject().location[2] / 100
        return int(result)

    def getYLocation(self, pourcent):
        result = pourcent * api.getFocusObject().location[3] / 100
        return int(result)

