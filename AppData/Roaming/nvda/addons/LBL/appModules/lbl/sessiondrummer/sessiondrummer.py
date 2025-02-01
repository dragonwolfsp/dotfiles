# Import des modules NVDA
import ui
from NVDAObjects.IAccessible import IAccessible
from scriptHandler import script

# Import des modules LBL
from ..api.navobject import NavObject
from ..api.ocr import LBLOCR
from ..api.mouse import Mouse
from .zones import drumZone, routingZone
from .tablist import TabList

class SessionDrummer(IAccessible):
    name = "LBL_SessionDrummer"
    drumZone = NavObject(drumZone, 3)
    tabList = NavObject(TabList)
    routingZone = NavObject(routingZone)
    mouse = Mouse()

    @script(gestures=["kb:tab", "kb:shift+tab"])
    def script_change_tab(self, gesture):
        ui.message(self.tabList.getNextObject(mouse = "move_and_click")["name"])

    @script(gesture="kb:enter")
    def script_click_on_piece(self, gesture):
        tab = self.tabList.getObject(mouse = None)["name"]

        if tab == "Drum":
            ui.message(self.drumZone.getObject(mouse = "move_and_click")["name"])
        elif tab == "Routing":
            ui.message(self.routingZone.getObject(mouse = "move_and_click")["name"])


    @script(gesture="kb:applications")
    def script_click_on_drum_button(self, gesture):
        tab = self.tabList.getObject(mouse = None)["name"]
        
        if tab == "Drum":
            self.mouse.moveAndLeftClick(x = 64, y = 526)

    @script(gesture="kb:leftarrow")
    def script_goToPreviousZone(self, gesture):
        tab = self.tabList.getObject(mouse = None)["name"]
        
        if tab == "Drum":
            ui.message(self.drumZone.getPreviousObject(mouse = "move_and_click")["name"])
        elif tab == "Routing":
            ui.message(self.routingZone.getPreviousObject(mouse = "move")["name"])

    @script(gesture="kb:rightarrow")
    def script_goToNextZone(self, gesture):
        tab = self.tabList.getObject(mouse = None)["name"]
        
        if tab == "Drum":
            ui.message(self.drumZone.getNextObject(mouse = "move_and_click")["name"])
        elif tab == "Routing":
            ui.message(self.routingZone.getNextObject(mouse = "move")["name"])

    @script(gesture="kb:k")
    def script_say_kit_name(self, gesture):
        tab = self.tabList.getObject(mouse = None)["name"]
        
        if tab == "Drum":
            ui.message(LBLOCR.getText([112, 517, 430, 533]))
    
    @script(gesture="kb:m")
    def script_click_on_midi_button(self, gesture):
        tab = self.tabList.getObject(mouse = None)["name"]
        
        if tab == "Drum":
            self.mouse.moveAndLeftClick(x = 64, y = 499)

    @script(gesture="kb:p")
    def script_click_on_program_button(self, gesture):
        tab = self.tabList.getObject(mouse = None)["name"]
        
        if tab == "Drum":
            self.mouse.moveAndLeftClick(x = 64, y = 474)

    @script(gesture="kb:t")
    def script_say_tab_name(self, gesture):
        ui.message(self.tabList.getObject(mouse = None)["name"])
