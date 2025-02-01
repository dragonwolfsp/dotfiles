# Import des modules Python
import time
import os

# Import des modules NVDA
import ui
import api
from NVDAObjects.IAccessible import IAccessible
from scriptHandler import script


# Import des modules LBL
from ..api.navobject import NavObject
from ..api.ocr import LBLOCR
from ..api.mouse import Mouse
from ..api import machine
from ..api import screen

if machine.get_machine_type() == "desktop":
    x = 171
    y = 20
    x_close = 955
    y_close = 81
elif machine.get_machine_type() == "laptop":
    x = 215
    y = 23
    x_close = 788
    y_close = 63


class Kontakt7(IAccessible):
    name = "LBL_Kontakt7"
    mouse = Mouse()
    previous_instrument = os.path.expanduser('~') + "\\AppData\\Roaming\\nvda\\addons\\LBL\\appModules\\lbl\\kontakt7\\images\\previous_instrument.png"
    next_instrument = os.path.expanduser('~') + "\\AppData\\Roaming\\nvda\\addons\\LBL\\appModules\\lbl\\kontakt7\\images\\next_instrument.png"
    previous_next_instrument = os.path.expanduser('~') + "\\AppData\\Roaming\\nvda\\addons\\LBL\\appModules\\lbl\\kontakt7\\images\\previous_next_instrument.png"

    @script(gestures=["kb:space", "kb:enter"])
    def script_defaultAction(self, gesture):
        global x
        global y

        self.mouse.moveCursor(x, y)
        self.mouse.leftClick()

    @script(gestures=["kb:leftarrow", "kb:p"])
    def script_load_previous_instrument(self, gesture):
        screen.locate_and_click(self.previous_next_instrument, xOffset = -5, xCleanMouse = 150, yCleanMouse = 150)
        time.sleep(0.5)
        self.mouse.moveCursor(10, 10)


    @script(gestures=["kb:rightarrow", "kb:n"])
    def script_load_next_instrument(self, gesture):
        screen.locate_and_click(self.previous_next_instrument, xOffset = 15, xCleanMouse = 50, yCleanMouse = 50)
        time.sleep(0.5)
        self.mouse.moveCursor(10, 10)


    @script(gesture="kb:delete")
    def script_close_instrument(self, gesture):
        self.mouse.moveAndLeftClick(x_close, y_close)
        ui.message("Instrument closed")
