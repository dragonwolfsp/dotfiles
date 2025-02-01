# Import des modules Python
import winUser
import time

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
from ..api.menu import Menu
from ..api.mouse import Mouse
from ..api import machine

# Import des modules propres à Steeven Slate Drummer 5
from .zonelist import zoneList
if machine.get_machine_type() == "desktop":
    from .modules.desktop.tablist import tabList
    from .modules.desktop.createmodule import createObject, resetColumns, resetCol1, resetCol2, resetCol3
    from .modules.desktop.drummodule import drumObject
    from .modules.desktop.mixermodule import mixerObject, overHeadObject, mixerTypeList, roomObject, roomBObject, SLRObject
    from .modules.desktop.mapmodule import mapObject
elif machine.get_machine_type() == "laptop":
    from .modules.laptop.tablist import tabList
    from .modules.laptop.createmodule import createObject, resetColumns, resetCol1, resetCol2, resetCol3
    from .modules.laptop.drummodule import drumObject
    from .modules.laptop.mixermodule import mixerObject, overHeadObject, mixerTypeList, roomObject, roomBObject, SLRObject
    from .modules.laptop.mapmodule import mapObject

class SteevenSlateDrummer(IAccessible):
    name = "Steeven Slate Drum 5"
    mouse = Mouse()
    role = "LBL_WINDOW"
    zone = NavObject(zoneList)
    tab = NavObject(tabList)
    createObject = NavObject(createObject)
    drumObject = NavObject(drumObject, 3)
    mixerObject = NavObject(mixerObject, 0)
    mapObject = NavObject(mapObject)
    overHeadObject = NavObject(overHeadObject)
    roomObject = NavObject(roomObject)
    roomBObject = NavObject(roomBObject)
    SLRObject = NavObject(SLRObject)
    mixerTypeList = NavObject(mixerTypeList)

    mode = "default"

    @script(gesture="kb:tab")
    def script_goToNextZone(self, gesture):
        """
            Définition du comportement de la touche tab, selon la zone
        """
        
        if self.mode == "default":
            ui.message(self.zone.getNextObject())

    @script(gesture="kb:shift+tab")
    def script_goToPreviousZone(self, gesture):
        """
            Définition du comportement des touches shift+tab, selon la zone
        """

        if self.mode == "default":
            ui.message(self.zone.getPreviousObject())

    @script(gesture="kb:rightarrow")
    def script_goToNextItem(self, gesture):
        """
            Définition du comportement de la touche flèche droite, selon la zone
        """
        
        zone = self.zone.getObject()
        tab = self.tab.getObject()
        mixerType = self.mixerTypeList.getObject()

        if zone == "Tabs":
            ui.message(self.tab.getNextObject(mouse = "move_and_click")["name"])
        elif zone == "Content":
            if tab["name"] == "Create":
                if self.mode == "default":
                    ui.message(self.createObject.getNextObject()["name"])
                elif self.mode == "library select":
                    self.mode = "category select"
                    ui.message("Category")
                    ui.message(self.createObject.getObject()["category"]())
                elif self.mode == "category select":
                    self.mode = "preset select"
                    ui.message("Kit presets")
                    ui.message(self.createObject.getObject()["preset"]())
            elif tab["name"] == "Drum":
                if self.mode == "default":
                    ui.message(self.drumObject.getNextObject(mouse = "move_and_click")["name"])
                elif self.mode == "piece_settings":
                    ui.message(self.drumObject.getSubObject()[1]("right", self.drumObject.getObject()["x"], self.drumObject.getObject()["y"]))
            elif tab["name"] == "Mixer":
                if self.mode == "default":
                    if mixerType["name"] == "Pieces":
                        ui.message(self.mixerObject.getNextObject(mouse = "move_and_click")["name"])
                    elif mixerType["name"] == "Over Heads":
                        ui.message(self.overHeadObject.getNextObject(mouse = "move_and_click")["name"])
                    elif mixerType["name"] == "Room":
                        ui.message(self.roomObject.getNextObject(mouse = "move_and_click")["name"])
                    elif mixerType["name"] == "Room B":
                        ui.message(self.roomBObject.getNextObject(mouse = "move_and_click")["name"])
                    elif mixerType["name"] == "SLR":
                        ui.message(self.SLRObject.getNextObject(mouse = "move_and_click")["name"])
            elif tab["name"] == "Map":
                ui.message(self.mapObject.getNextObject())

    @script(gesture="kb:leftarrow")
    def script_goToPreviousItem(self, gesture):
        """
            Définition du comportement de la touche flèche gauche, selon la zone
        """

        zone = self.zone.getObject()
        tab = self.tab.getObject()
        mixerType = self.mixerTypeList.getObject()

        if zone == "Tabs":
            ui.message(self.tab.getPreviousObject(mouse = "move_and_click")["name"])
        elif zone == "Content":
            if tab["name"] == "Create":
                if self.mode == "default":
                    ui.message(self.createObject.getPreviousObject()["name"])
                elif self.mode == "category select":
                    resetCol2()
                    self.mode = "library select"
                    ui.message("Library")
                    ui.message(self.createObject.getObject()["library"]())
                elif self.mode == "preset select":
                    resetCol3()
                    self.mode = "category select"
                    ui.message("Category")
                    ui.message(self.createObject.getObject()["category"]())
            elif tab["name"] == "Drum":
                if self.mode == "default":
                    ui.message(self.drumObject.getPreviousObject(mouse = "move_and_click")["name"])
                elif self.mode == "piece_settings":
                    ui.message(self.drumObject.getSubObject()[1]("left", self.drumObject.getObject()["x"], self.drumObject.getObject()["y"]))
            elif tab["name"] == "Mixer":
                if self.mode == "default":
                    if mixerType["name"] == "Pieces":
                        ui.message(self.mixerObject.getPreviousObject(mouse = "move_and_click")["name"])
                    elif mixerType["name"] == "Over Heads":
                        ui.message(self.overHeadObject.getPreviousObject(mouse = "move_and_click")["name"])
                    elif mixerType["name"] == "Room":
                        ui.message(self.roomObject.getPreviousObject(mouse = "move_and_click")["name"])
                    elif mixerType["name"] == "Room B":
                        ui.message(self.roomBObject.getPreviousObject(mouse = "move_and_click")["name"])
                    elif mixerType["name"] == "SLR":
                        ui.message(self.SLRObject.getPreviousObject(mouse = "move_and_click")["name"])
            elif tab["name"] == "Map":
                ui.message(self.mapObject.getPreviousObject())
    @script(gesture="kb:uparrow")
    def script_goToUpItem(self, gesture):
        """
            Définition du comportement de la touche flèche haut, selon la zone
        """

        zone = self.zone.getObject()
        tab = self.tab.getObject()
        drumObject = self.drumObject.getObject()
        mixerType = self.mixerTypeList.getObject()
        piecesMics = self.mixerObject.getObject()
        overheads = self.overHeadObject.getObject()
        room = self.roomObject.getObject()
        roomB = self.roomBObject.getObject()
        SLR = self.SLRObject.getObject()
        
        if zone == "Content":
            if tab["name"] == "Drum":
                if self.mode == "piece_settings":
                    ui.message(self.drumObject.getPreviousSubObject()[0])
            elif tab["name"] == "Mixer":
                if self.mode == "default":
                    ui.message(self.mixerTypeList.getPreviousObject()["name"])
                    if mixerType["name"] == "Over Heads":
                        ui.message(self.mixerObject.getObject(mouse = "move_and_click")["name"])
                    elif mixerType["name"] == "Room":
                        ui.message(self.overHeadObject.getObject(mouse = "move_and_click")["name"])
                    elif mixerType["name"] == "Pieces":
                        ui.message(self.SLRObject.getObject(mouse = "move_and_click")["name"])
                    elif mixerType["name"] == "Room B":
                        ui.message(self.roomObject.getObject(mouse = "move_and_click")["name"])
                    elif mixerType["name"] == "SLR":
                        ui.message(self.roomBObject.getObject(mouse = "move_and_click")["name"])
                if self.mode == "menu":
                    if mixerType["name"] == "Pieces":
                        ui.message(piecesMics["routing"]("up", menuSize = piecesMics["menuSize"]))
                    elif mixerType["name"] == "Over Heads":
                        ui.message(overheads["routing"]("up", menuSize = overheads["menuSize"]))
                    elif mixerType["name"] == "Room":
                        ui.message(room["routing"]("up", menuSize = room["menuSize"]))
                    elif mixerType["name"] == "Room B":
                        ui.message(roomB["routing"]("up", menuSize = roomB["menuSize"]))
                    elif mixerType["name"] == "SLR":
                        ui.message(SLR["routing"]("up", menuSize = SLR["menuSize"]))
                    keyboardHandler.KeyboardInputGesture.fromName("uparrow").send()
            elif tab["name"] == "Create" and self.mode != "default":
                if self.mode == "library select":
                    ui.message(str(self.createObject.getObject()["library"](key = "up", libraryNumber = self.createObject.getObject()["libraryNumber"]())))
                elif self.mode == "category select":
                    ui.message(str(self.createObject.getObject()["category"](key = "up", categoryNumber = self.createObject.getObject()["categoryNumber"]())))
                elif self.mode == "preset select":
                    ui.message(str(self.createObject.getObject()["preset"](key = "up", presetNumber = self.createObject.getObject()["presetNumber"]())))

    @script(gesture="kb:downarrow")
    def script_goToDownItem(self, gesture):
        """
            Définition du comportement de la touche flèche bas, selon la zone
        """

        zone = self.zone.getObject()
        tab = self.tab.getObject()
        drumObject = self.drumObject.getObject()
        mixerType = self.mixerTypeList.getObject()
        piecesMics = self.mixerObject.getObject()
        overheads = self.overHeadObject.getObject()
        room = self.roomObject.getObject()
        roomB = self.roomBObject.getObject()
        SLR = self.SLRObject.getObject()

        if zone == "Content":
            if tab["name"] == "Drum":
                if self.mode == "default":
                    self.mode = "piece_settings"
                    ui.message(self.drumObject.getObject()["name"] + "Configuration, " + self.drumObject.getSubObject()[0])
                elif self.mode == "piece_settings":
                    ui.message(self.drumObject.getNextSubObject()[0])
            elif tab["name"] == "Mixer":
                if self.mode == "default":
                    ui.message(self.mixerTypeList.getNextObject()["name"])
                    if mixerType["name"] == "Room":
                        ui.message(self.roomBObject.getObject(mouse = "move_and_click")["name"])
                    elif mixerType["name"] == "Pieces":
                        ui.message(self.overHeadObject.getObject(mouse = "move_and_click")["name"])
                    elif mixerType["name"] == "Over Heads":
                        ui.message(self.roomObject.getObject(mouse = "move_and_click")["name"])
                    elif mixerType["name"] == "Room B":
                        ui.message(self.SLRObject.getObject(mouse = "move_and_click")["name"])
                    elif mixerType["name"] == "SLR":
                        ui.message(self.mixerObject.getObject(mouse = "move_and_click")["name"])
                if self.mode == "menu":
                    if mixerType["name"] == "Pieces":
                        ui.message(piecesMics["routing"]("down", menuSize = piecesMics["menuSize"]))
                    elif mixerType["name"] == "Over Heads":
                        ui.message(overheads["routing"]("down", menuSize = overheads["menuSize"]))
                    elif mixerType["name"] == "Room":
                        ui.message(room["routing"]("down", menuSize = room["menuSize"]))
                    elif mixerType["name"] == "Room B":
                        ui.message(roomB["routing"]("down", menuSize = room["menuSize"]))
                    elif mixerType["name"] == "SLR":
                        ui.message(roomB["routing"]("down", menuSize = SLR["menuSize"]))
                    keyboardHandler.KeyboardInputGesture.fromName("downarrow").send()
            elif tab["name"] == "Create" and self.mode != "default":
                if self.mode == "library select":
                    ui.message(str(self.createObject.getObject()["library"](key = "down", libraryNumber = self.createObject.getObject()["libraryNumber"]())))
                elif self.mode == "category select":
                    ui.message(str(self.createObject.getObject()["category"](key = "down", categoryNumber = self.createObject.getObject()["categoryNumber"]())))
                elif self.mode == "preset select":
                    ui.message(str(self.createObject.getObject()["preset"](key = "down", presetNumber = self.createObject.getObject()["presetNumber"]())))

    @script(gesture="kb:shift+uparrow")
    def script_volumeUp(self, gesture):
        zone = self.zone.getObject()
        tab = self.tab.getObject()
        mixerType = self.mixerTypeList.getObject()
        piecesMics = self.mixerObject.getObject()
        overheads = self.overHeadObject.getObject()
        room = self.roomObject.getObject()
        roomB = self.roomBObject.getObject()
        SLR = self.SLRObject.getObject()

        if zone == "Content":
            if tab["name"] == "Mixer":
                if mixerType["name"] == "Pieces":
                    piecesMics["volume"]("up", piecesMics["volumeX"], piecesMics["volumeY"], piecesMics["x"], piecesMics["y"], piecesMics["scroll"])
                elif mixerType["name"] == "Over Heads":
                    overheads["volume"]("up", overheads["volumeX"], overheads["volumeY"], overheads["x"], overheads["y"], overheads["scroll"])
                elif mixerType["name"] == "Room":
                    room["volume"]("up", room["volumeX"], room["volumeY"], room["x"], room["y"], room["scroll"])
                elif mixerType["name"] == "Room B":
                    roomB["volume"]("up", roomB["volumeX"], roomB["volumeY"], roomB["x"], roomB["y"], roomB["scroll"])
                elif mixerType["name"] == "SLR":
                    SLR["volume"]("up", SLR["volumeX"], SLR["volumeY"], SLR["x"], SLR["y"], SLR["scroll"])
            
    @script(gesture="kb:shift+downarrow")
    def script_volumeDown(self, gesture):
        zone = self.zone.getObject()
        tab = self.tab.getObject()
        mixerType = self.mixerTypeList.getObject()
        piecesMics = self.mixerObject.getObject()
        overheads = self.overHeadObject.getObject()
        room = self.roomObject.getObject()
        roomB = self.roomBObject.getObject()
        SLR = self.SLRObject.getObject()

        if zone == "Content":
            if tab["name"] == "Mixer":
                if mixerType["name"] == "Pieces":
                    piecesMics["volume"]("down", piecesMics["volumeX"], piecesMics["volumeY"], piecesMics["x"], piecesMics["y"], piecesMics["scroll"])
                elif mixerType["name"] == "Over Heads":
                    overheads["volume"]("down", overheads["volumeX"], overheads["volumeY"], overheads["x"], overheads["y"], overheads["scroll"])
                elif mixerType["name"] == "Room":
                    room["volume"]("down", room["volumeX"], room["volumeY"], room["x"], room["y"], room["scroll"])
                elif mixerType["name"] == "Room B":
                    roomB["volume"]("down", roomB["volumeX"], roomB["volumeY"], roomB["x"], roomB["y"], roomB["scroll"])
                elif mixerType["name"] == "SLR":
                    SLR["volume"]("down", SLR["volumeX"], SLR["volumeY"], SLR["x"], SLR["y"], SLR["scroll"])

    @script(gesture="kb:shift+leftarrow")
    def script_panoramicLeft(self, gesture):
        zone = self.zone.getObject()
        tab = self.tab.getObject()
        mixerType = self.mixerTypeList.getObject()
        piecesMics = self.mixerObject.getObject()
        overheads = self.overHeadObject.getObject()
        room = self.roomObject.getObject()
        roomB = self.roomBObject.getObject()
        SLR = self.SLRObject.getObject()

        if zone == "Content":
            if tab["name"] == "Mixer":
                if mixerType["name"] == "Pieces":
                    piecesMics["panoramic"]("left", piecesMics["panoramicX"], piecesMics["panoramicY"], piecesMics["x"], piecesMics["y"], piecesMics["scroll"])
                elif mixerType["name"] == "Over Heads":
                    overheads["panoramic"]("left", overheads["panoramicX"], overheads["panoramicY"], overheads["x"], overheads["y"], overheads["scroll"])
                elif mixerType["name"] == "Room":
                    room["panoramic"]("left", room["panoramicX"], room["panoramicY"], room["x"], room["y"], room["scroll"])
                elif mixerType["name"] == "Room B":
                    roomB["panoramic"]("left", roomB["panoramicX"], roomB["panoramicY"], roomB["x"], roomB["y"], roomB["scroll"])
                elif mixerType["name"] == "SLR":
                    SLR["panoramic"]("left", SLR["panoramicX"], SLR["panoramicY"], SLR["x"], SLR["y"], SLR["scroll"])

    @script(gesture="kb:shift+rightarrow")
    def script_panoramicRight(self, gesture):
        zone = self.zone.getObject()
        tab = self.tab.getObject()
        mixerType = self.mixerTypeList.getObject()
        piecesMics = self.mixerObject.getObject()
        overheads = self.overHeadObject.getObject()
        room = self.roomObject.getObject()
        roomB = self.roomBObject.getObject()
        SLR = self.SLRObject.getObject()

        if zone == "Content":
            if tab["name"] == "Mixer":
                if mixerType["name"] == "Pieces":
                    piecesMics["panoramic"]("right", piecesMics["panoramicX"], piecesMics["panoramicY"], piecesMics["x"], piecesMics["y"], piecesMics["scroll"])
                elif mixerType["name"] == "Over Heads":
                    overheads["panoramic"]("right", overheads["panoramicX"], overheads["panoramicY"], overheads["x"], overheads["y"], overheads["scroll"])
                elif mixerType["name"] == "Room":
                    room["panoramic"]("right", room["panoramicX"], room["panoramicY"], room["x"], room["y"], room["scroll"])
                elif mixerType["name"] == "Room B":
                    roomB["panoramic"]("right", roomB["panoramicX"], roomB["panoramicY"], roomB["x"], roomB["y"], roomB["scroll"])
                elif mixerType["name"] == "SLR":
                    SLR["panoramic"]("right", SLR["panoramicX"], SLR["panoramicY"], SLR["x"], SLR["y"], SLR["scroll"])

    @script(gesture="kb:enter")
    def script_getTab(self, gesture):
        """
            Définition du comportement de la touche entrée
        """

        zone = self.zone.getObject()
        tab = self.tab.getObject()
        mixerType = self.mixerTypeList.getObject()
        piecesMics = self.mixerObject
        overheads = self.overHeadObject
        room = self.roomObject
        roomB = self.roomBObject
        SLR = self.SLRObject

        if zone == "Content":
            if tab["name"] == "Drum":
                if self.mode == "default":
                    self.drumObject.getObject(mouse = "move_and_click")["name"]
                elif self.mode == "piece_settings":
                    ui.message(self.drumObject.getObject()["name"] + " configuration saved")
                    self.mode = "default"
            elif tab["name"] == "Mixer":
                if self.mode == "default":
                    if mixerType["name"] == "Pieces":
                        piecesMics.getObject(mouse = "move_and_click")["name"]
                    elif mixerType["name"] == "Over Heads":
                        overheads.getObject(mouse = "move_and_click")["name"]
                    elif mixerType["name"] == "Room":
                        room.getObject(mouse = "move_and_click")["name"]
                    elif mixerType["name"] == "Room B":
                        roomB.getObject(mouse = "move_and_click")["name"]
                    elif mixerType["name"] == "SLR":
                        SLR.getObject(mouse = "move_and_click")["name"]
                elif self.mode == "menu":
                    ui.message("Routing saved")
                    keyboardHandler.KeyboardInputGesture.fromName("enter").send()
                    self.mode = "default"
            elif tab["name"] == "Create":
                if self.createObject.getObject()["name"] == "Kits":
                    if self.mode == "default":
                        ui.message(str(self.createObject.getObject()["library"](key = "enter", libraryNumber = self.createObject.getObject()["libraryNumber"]())))
                        self.mode = "library select"
                    elif self.mode == "library select":
                        self.mode = "category select"
                        ui.message("Category")
                        ui.message(self.createObject.getObject()["category"]())
                    elif self.mode == "category select":
                        self.mode = "preset select"
                        ui.message("Kit presets")
                        ui.message(self.createObject.getObject()["preset"]())
                    elif self.mode == "preset select":
                        self.mouse.doubleClick()
                        self.mode = "default"
                        resetColumns()
                        ui.message("Kit preset selected")
            elif tab["name"] == "Map":
                if self.mode == "default":
                    if self.mapObject.getObject() == "resetMap":
                        self.mouse.moveAndLeftClick(190, 620)
                    elif self.mapObject.getObject() == "loadMap":
                        self.mouse.moveAndLeftClick(880, 620)
                        self.mode = "load map"
                elif self.mode == "load map":
                    keyboardHandler.KeyboardInputGesture.fromName("enter").send()
                    ui.message("Map selected")
                    self.mode = "default"


    @script(gesture="kb:escape")
    def script_closeFxWindow(self, gesture):
        """
            Définition du comportement de la touche Echape
        """

        if self.mode == "default":
            self.zone.resetObject()
            self.tab.resetObject()
            self.createObject.resetObject()
            self.drumObject.resetObject()
            self.mixerTypeList.resetObject()
            self.mixerObject.resetObject()
            self.overHeadObject.resetObject()
            self.roomObject.resetObject()
            self.mixerObject.resetObject()
            self.SLRObject.resetObject()
            config.conf["mouse"]["enableMouseTracking"] = True
            keyboardHandler.KeyboardInputGesture.fromName("escape").send()
        elif self.mode == "piece_settings":
            self.drumObject.paramsPosition = self.drumObject.defaultParamsPosition
            ui.message(self.drumObject.getObject()["name"] + " configuration saved")
            self.mode = "default"
        elif self.mode == "menu":
            ui.message("Cancel")
            keyboardHandler.KeyboardInputGesture.fromName("escape").send()
            self.mode = "default"
        elif self.mode in ["library select", "category select", "preset select"]:
            resetColumns()
            ui.message("Kit selection canceled")
            self.mode = "default"

    @script(gesture="kb:applications")
    def script_applicationMenu(self, gesture):
        tab = self.tab.getObject()
        zone = self.zone.getObject()
        piecesMics = self.mixerObject.getObject()
        mixerType = self.mixerTypeList.getObject()
        overheads = self.overHeadObject.getObject()
        room = self.roomObject.getObject()
        roomB = self.roomBObject.getObject()
        SLR = self.SLRObject.getObject()

        if zone == "Content":
            if tab["name"] == "Drum":
                if self.mode == "default":
                    self.mode = "piece_settings"
                    ui.message(self.drumObject.getObject()["name"] + "Configuration, " + self.drumObject.getSubObject()[0])
            elif tab["name"] == "Mixer":
                if self.mode == "default":
                    self.mode = "menu"
                    if mixerType["name"] == "Pieces":
                        ui.message(piecesMics["routing"]("enter", piecesMics["routingButtonX"], piecesMics["routingButtonY"], piecesMics["routingDiagonal"], piecesMics["menuSize"], piecesMics["scroll"]))
                    elif mixerType["name"] == "Over Heads":
                        ui.message(overheads["routing"]("enter", overheads["routingButtonX"], overheads["routingButtonY"], overheads["routingDiagonal"], overheads["menuSize"], overheads["scroll"]))
                    elif mixerType["name"] == "Room":
                        ui.message(room["routing"]("enter", room["routingButtonX"], room["routingButtonY"], room["routingDiagonal"], room["menuSize"], room["scroll"]))
                    elif mixerType["name"] == "Room B":
                        ui.message(roomB["routing"]("enter", roomB["routingButtonX"], roomB["routingButtonY"], roomB["routingDiagonal"], roomB["menuSize"], roomB["scroll"]))
                    elif mixerType["name"] == "SLR":
                        ui.message(SLR["routing"]("enter", SLR["routingButtonX"], SLR["routingButtonY"], SLR["routingDiagonal"], SLR["menuSize"], SLR["scroll"]))

    @script(gesture="kb:NVDA+d")
    def script_debug(self, gesture):
        ui.message(self.mode)

