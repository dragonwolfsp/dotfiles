import time
import ui
from ....api.mouse import Mouse
from ....api.navobject import NavObject
from ....api.ocr import LBLOCR
from ...ocrdictionnary import ocrDictionnary
from ...routingmenu32 import routingMenu32
from ...routingmenu36 import routingMenu36

mouse = Mouse()
menu32 = NavObject(routingMenu32)
menu36 = NavObject(routingMenu36)

def setVolume(key = None, volumeX = 0, volumeY = 0, pieceX = 0, pieceY = 0, scroll = 0):
    mouse.moveAndScroll(172, 307, scroll)
    if key == "up":
        mouse.moveAndScroll(volumeX, volumeY, 20)
        mouse.moveAndLeftClick(pieceX, pieceY)
    elif key == "down":
        mouse.moveAndScroll(volumeX, volumeY, -20)
        mouse.moveAndLeftClick(pieceX, pieceY)

def setPanoramic(key = None, panoramicX = 0, panoramicY = 0, pieceX = 0, pieceY = 0, scroll = 0):
    mouse.moveAndScroll(172, 307, scroll)
    if key == "left":
        mouse.moveAndScroll(panoramicX, panoramicY, -20)
        mouse.moveAndLeftClick(pieceX, pieceY)
    elif key == "right":
        mouse.moveAndScroll(panoramicX, panoramicY, 20)
        mouse.moveAndLeftClick(pieceX, pieceY)

def setState(diagonal = []):
    color = LBLOCR.getColor(diagonal)

    if color == "#59caf5":
        state = "Muté"
    elif color == "#143650":
        state = "Non muté"
    else:
        return "Etat Inconnu"
    mouse.moveAndLeftClick(diagonal[0], diagonal[1])
    return state

def setRouting(key = None, routingButtonX = 0, routingButtonY = 0, ocrDiagonal = [], menuSize = 0, scroll = 0):
    mouse.moveAndScroll(172, 307, scroll)
    if menuSize == 32:
        menu = menu32
    elif menuSize == 36:
        menu = menu36

    if key == "enter":
        ocrResult = LBLOCR.getText(ocrDiagonal)
        selectedItem = LBLOCR.getCorrection(ocrResult, ocrDictionnary)
        mouse.moveAndLeftClick(routingButtonX, routingButtonY)
        menu.goToObjectByName(selectedItem)
        
        return selectedItem

    elif key == "up":
        return menu.getPreviousObject()
    elif key == "down":
        return menu.getNextObject()

kickInParams = {
    "name": "Kick In",
    "x": 641,
    "y": 670,
    "stateDiagonal": [157, 195, 158, 196],
    "volumeX": 458,
    "volumeY": 195,
    "volumeDiagonal": [478, 185, 528, 205],
    "panoramicX": 548,
    "panoramicY": 195,
    "panoramicDiagonal": [568, 185, 618, 205],
    "routingButtonX": 420,
    "routingButtonY": 195,
    "routingDiagonal": [309, 185, 444, 205],
    "menuSize": 32,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

kickOutParams = {
    "name": "Kick Out",
    "x": 641,
    "y": 670,
    "stateDiagonal": [],
    "volumeX": 458,
    "volumeY": 225,
    "volumeDiagonal": [478, 215, 528, 235],
    "panoramicX": 548,
    "panoramicY": 235,
    "panoramicDiagonal": [568, 215, 618, 235],
    "routingButtonX": 420,
    "routingButtonY": 225,
    "routingDiagonal": [309, 215, 444, 235],
    "menuSize": 32,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

kickOHParams = {
    "name": "Kick Over Head",
    "x": 641,
    "y": 670,
    "stateDiagonal": [157, 255, 158, 256],
    "volumeX": 458,
    "volumeY": 255,
    "volumeDiagonal": [478, 245, 528, 265],
    "panoramicX": 548,
    "panoramicY": 255,
    "panoramicDiagonal": [568, 215, 618, 235],
    "routingButtonX": 420,
    "routingButtonY": 255,
    "routingDiagonal": [309, 245, 444, 265],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

kickRoomParams = {
    "name": "Kick Room",
    "x": 641,
    "y": 670,
    "stateDiagonal": [157, 285, 158, 286],
    "volumeX": 458,
    "volumeY": 285,
    "volumeDiagonal": [478, 275, 528, 295],
    "panoramicX": 548,
    "panoramicY": 285,
    "panoramicDiagonal": [568, 275, 618, 295],
    "routingButtonX": 420,
    "routingButtonY": 285,
    "routingDiagonal": [309, 275, 444, 295],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

kickRoomBParams = {
    "name": "Kick Room B",
    "x": 641,
    "y": 670,
    "stateDiagonal": [157, 315, 158, 316],
    "volumeX": 458,
    "volumeY": 315,
    "volumeDiagonal": [478, 305, 528, 325],
    "panoramicX": 548,
    "panoramicY": 315,
    "panoramicDiagonal": [568, 305, 618, 325],
    "routingButtonX": 420,
    "routingButtonY": 315,
    "routingDiagonal": [309, 305, 444, 325],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

kickSLRParams = {
    "name": "Kick SLR",
    "x": 641,
    "y": 670,
    "stateDiagonal": [157, 315, 158, 316],
    "volumeX": 458,
    "volumeY": 315,
    "volumeDiagonal": [478, 305, 528, 325],
    "panoramicX": 548,
    "panoramicY": 315,
    "panoramicDiagonal": [568, 305, 618, 325],
    "routingButtonX": 420,
    "routingButtonY": 315,
    "routingDiagonal": [309, 305, 444, 325],
    "menuSize": 36,
    "scroll": -75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

snareTopParams = {
    "name": "Snare Top",
    "x": 547 ,
    "y": 613,
    "stateDiagonal": [157, 195, 158, 196],
    "volumeX": 458,
    "volumeY": 195,
    "volumeDiagonal": [478, 185, 528, 205],
    "panoramicX": 548,
    "panoramicY": 195,
    "panoramicDiagonal": [568, 185, 618, 205],
    "routingButtonX": 420,
    "routingButtonY": 195,
    "routingDiagonal": [309, 185, 444, 205],
    "menuSize": 32,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

snareBottomParams = {
    "name": "Snare Bottom",
    "x": 547 ,
    "y": 613,
    "stateDiagonal": [157, 195, 158, 196],
    "volumeX": 458,
    "volumeY": 225,
    "volumeDiagonal": [478, 215, 528, 235],
    "panoramicX": 548,
    "panoramicY": 235,
    "panoramicDiagonal": [568, 215, 618, 235],
    "routingButtonX": 420,
    "routingButtonY": 225,
    "routingDiagonal": [309, 215, 444, 235],
    "menuSize": 32,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

snareRNGParams = {
    "name": "Snare Ring",
    "x": 547 ,
    "y": 613,
    "stateDiagonal": [157, 255, 158, 256],
    "volumeX": 458,
    "volumeY": 255,
    "volumeDiagonal": [478, 245, 528, 265],
    "panoramicX": 548,
    "panoramicY": 255,
    "panoramicDiagonal": [568, 215, 618, 235],
    "routingButtonX": 420,
    "routingButtonY": 255,
    "routingDiagonal": [309, 245, 444, 265],
    "menuSize": 32,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

snareOHParams = {
    "name": "Snare Over Head",
    "x": 547 ,
    "y": 613,
    "stateDiagonal": [157, 285, 158, 286],
    "volumeX": 458,
    "volumeY": 285,
    "volumeDiagonal": [478, 275, 528, 295],
    "panoramicX": 548,
    "panoramicY": 285,
    "panoramicDiagonal": [568, 275, 618, 295],
    "routingButtonX": 420,
    "routingButtonY": 285,
    "routingDiagonal": [309, 275, 444, 295],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

snareRoomParams = {
    "name": "Snare Room",
    "x": 547 ,
    "y": 613,
    "stateDiagonal": [157, 315, 158, 316],
    "volumeX": 458,
    "volumeY": 315,
    "volumeDiagonal": [478, 305, 528, 325],
    "panoramicX": 548,
    "panoramicY": 315,
    "panoramicDiagonal": [568, 305, 618, 325],
    "routingButtonX": 420,
    "routingButtonY": 315,
    "routingDiagonal": [309, 305, 444, 325],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

snareRoomBParams = {
    "name": "Snare Room B",
    "x": 547 ,
    "y": 613,
    "stateDiagonal": [157, 315, 158, 316],
    "volumeX": 458,
    "volumeY": 315,
    "volumeDiagonal": [478, 305, 528, 325],
    "panoramicX": 548,
    "panoramicY": 315,
    "panoramicDiagonal": [568, 305, 618, 325],
    "routingButtonX": 420,
    "routingButtonY": 315,
    "routingDiagonal": [309, 305, 444, 325],
    "menuSize": 36,
    "scroll": -75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

tom1Params = {
    "name": "Tom 1",
    "x": 550,
    "y": 544,
    "stateDiagonal": [157, 195, 158, 196],
    "stateDiagonal": [],
    "volumeX": 458,
    "volumeY": 195,
    "volumeDiagonal": [478, 185, 528, 205],
    "panoramicX": 548,
    "panoramicY": 195,
    "panoramicDiagonal": [568, 185, 618, 205],
    "routingButtonX": 420,
    "routingButtonY": 195,
    "routingDiagonal": [309, 185, 444, 205],
    "menuSize": 32,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

tom1OHParams = {
    "name": "Tom 1 Over Head",
    "x": 550,
    "y": 544,
    "stateDiagonal": [],
    "volumeX": 458,
    "volumeY": 225,
    "volumeDiagonal": [478, 215, 528, 235],
    "panoramicX": 548,
    "panoramicY": 235,
    "panoramicDiagonal": [568, 215, 618, 235],
    "routingButtonX": 420,
    "routingButtonY": 225,
    "routingDiagonal": [309, 215, 444, 235],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

tom1RoomParams = {
    "name": "Tom 1 Room",
    "x": 550,
    "y": 544,
    "stateDiagonal": [157, 255, 158, 256],
    "volumeX": 458,
    "volumeY": 255,
    "volumeDiagonal": [478, 245, 528, 265],
    "panoramicX": 548,
    "panoramicY": 255,
    "panoramicDiagonal": [568, 215, 618, 235],
    "routingButtonX": 420,
    "routingButtonY": 255,
    "routingDiagonal": [309, 245, 444, 265],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

tom1RoomBParams = {
    "name": "Tom1 Room B",
    "x": 550,
    "y": 544,
    "stateDiagonal": [157, 285, 158, 286],
    "volumeX": 458,
    "volumeY": 285,
    "volumeDiagonal": [478, 275, 528, 295],
    "panoramicX": 548,
    "panoramicY": 285,
    "panoramicDiagonal": [568, 275, 618, 295],
    "routingButtonX": 420,
    "routingButtonY": 285,
    "routingDiagonal": [309, 275, 444, 295],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

tom1SLRParams = {
    "name": "Tom 1 SLR",
    "x": 550,
    "y": 544,
    "stateDiagonal": [157, 315, 158, 316],
    "volumeX": 458,
    "volumeY": 315,
    "volumeDiagonal": [478, 305, 528, 325],
    "panoramicX": 548,
    "panoramicY": 315,
    "panoramicDiagonal": [568, 305, 618, 325],
    "routingButtonX": 420,
    "routingButtonY": 315,
    "routingDiagonal": [309, 305, 444, 325],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

tom2Params = {
    "name": "Tom 2",
    "x": 626,
    "y": 526,
    "stateDiagonal": [157, 195, 158, 196],
    "volumeX": 458,
    "volumeY": 195,
    "volumeDiagonal": [478, 185, 528, 205],
    "panoramicX": 548,
    "panoramicY": 195,
    "panoramicDiagonal": [568, 185, 618, 205],
    "routingButtonX": 420,
    "routingButtonY": 195,
    "routingDiagonal": [309, 185, 444, 205],
    "menuSize": 32,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

tom2OHParams = {
    "name": "Tom 2 Over Head",
    "x": 626,
    "y": 526,
    "stateDiagonal": [],
    "volumeX": 458,
    "volumeY": 225,
    "volumeDiagonal": [478, 215, 528, 235],
    "panoramicX": 548,
    "panoramicY": 235,
    "panoramicDiagonal": [568, 215, 618, 235],
    "routingButtonX": 420,
    "routingButtonY": 225,
    "routingDiagonal": [309, 215, 444, 235],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

tom2RoomParams = {
    "name": "Tom 2 Room",
    "x": 626,
    "y": 526,
    "stateDiagonal": [157, 255, 158, 256],
    "volumeX": 458,
    "volumeY": 255,
    "volumeDiagonal": [478, 245, 528, 265],
    "panoramicX": 548,
    "panoramicY": 255,
    "panoramicDiagonal": [568, 215, 618, 235],
    "routingButtonX": 420,
    "routingButtonY": 255,
    "routingDiagonal": [309, 245, 444, 265],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

tom2RoomBParams = {
    "name": "Tom 2 Room B",
    "x": 626,
    "y": 526,
    "stateDiagonal": [157, 285, 158, 286],
    "volumeX": 458,
    "volumeY": 285,
    "volumeDiagonal": [478, 275, 528, 295],
    "panoramicX": 548,
    "panoramicY": 285,
    "panoramicDiagonal": [568, 275, 618, 295],
    "routingButtonX": 420,
    "routingButtonY": 285,
    "routingDiagonal": [309, 275, 444, 295],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

tom2SLRParams = {
    "name": "Tom 2 SLR",
    "x": 626,
    "y": 526,
    "stateDiagonal": [157, 315, 158, 316],
    "volumeX": 458,
    "volumeY": 315,
    "volumeDiagonal": [478, 305, 528, 325],
    "panoramicX": 548,
    "panoramicY": 315,
    "panoramicDiagonal": [568, 305, 618, 325],
    "routingButtonX": 420,
    "routingButtonY": 315,
    "routingDiagonal": [309, 305, 444, 325],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

tom3Params = {
    "name": "Tom 3",
    "x": 758,
    "y": 610,
    "stateDiagonal": [157, 195, 158, 196],
    "volumeX": 458,
    "volumeY": 195,
    "volumeDiagonal": [478, 185, 528, 205],
    "panoramicX": 548,
    "panoramicY": 195,
    "panoramicDiagonal": [568, 185, 618, 205],
    "routingButtonX": 420,
    "routingButtonY": 195,
    "routingDiagonal": [309, 185, 444, 205],
    "menuSize": 32,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

tom3OHParams = {
    "name": "Tom 3 Over Head",
    "x": 758,
    "y": 610,
    "stateDiagonal": [],
    "volumeX": 458,
    "volumeY": 225,
    "volumeDiagonal": [478, 215, 528, 235],
    "panoramicX": 548,
    "panoramicY": 235,
    "panoramicDiagonal": [568, 215, 618, 235],
    "routingButtonX": 420,
    "routingButtonY": 225,
    "routingDiagonal": [309, 215, 444, 235],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

tom3RoomParams = {
    "name": "Tom 3 Room",
    "x": 758,
    "y": 610,
    "stateDiagonal": [157, 255, 158, 256],
    "volumeX": 458,
    "volumeY": 255,
    "volumeDiagonal": [478, 245, 528, 265],
    "panoramicX": 548,
    "panoramicY": 255,
    "panoramicDiagonal": [568, 215, 618, 235],
    "routingButtonX": 420,
    "routingButtonY": 255,
    "routingDiagonal": [309, 245, 444, 265],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

tom3RoomBParams = {
    "name": "Tom 3 Room B",
    "x": 758,
    "y": 610,
    "stateDiagonal": [157, 285, 158, 286],
    "volumeX": 458,
    "volumeY": 285,
    "volumeDiagonal": [478, 275, 528, 295],
    "panoramicX": 548,
    "panoramicY": 285,
    "panoramicDiagonal": [568, 275, 618, 295],
    "routingButtonX": 420,
    "routingButtonY": 285,
    "routingDiagonal": [309, 275, 444, 295],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

tom3SLRParams = {
    "name": "Tom 3 SLR",
    "x": 758,
    "y": 610,
    "stateDiagonal": [157, 315, 158, 316],
    "volumeX": 458,
    "volumeY": 315,
    "volumeDiagonal": [478, 305, 528, 325],
    "panoramicX": 548,
    "panoramicY": 315,
    "panoramicDiagonal": [568, 305, 618, 325],
    "routingButtonX": 420,
    "routingButtonY": 315,
    "routingDiagonal": [309, 305, 444, 325],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

tom4Params = {
    "name": "Tom 4",
    "x": 820,
    "y": 674,
    "stateDiagonal": [157, 195, 158, 196],
    "volumeX": 458,
    "volumeY": 195,
    "volumeDiagonal": [478, 185, 528, 205],
    "panoramicX": 548,
    "panoramicY": 195,
    "panoramicDiagonal": [568, 185, 618, 205],
    "routingButtonX": 420,
    "routingButtonY": 195,
    "routingDiagonal": [309, 185, 444, 205],
    "menuSize": 32,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

tom4OHParams = {
    "name": "Tom 4 Over Head",
    "x": 820,
    "y": 674,
    "stateDiagonal": [],
    "volumeX": 458,
    "volumeY": 225,
    "volumeDiagonal": [478, 215, 528, 235],
    "panoramicX": 548,
    "panoramicY": 235,
    "panoramicDiagonal": [568, 215, 618, 235],
    "routingButtonX": 420,
    "routingButtonY": 225,
    "routingDiagonal": [309, 215, 444, 235],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

tom4RoomParams = {
    "name": "Tom 4 Room",
    "x": 820,
    "y": 674,
    "stateDiagonal": [157, 255, 158, 256],
    "volumeX": 458,
    "volumeY": 255,
    "volumeDiagonal": [478, 245, 528, 265],
    "panoramicX": 548,
    "panoramicY": 255,
    "panoramicDiagonal": [568, 215, 618, 235],
    "routingButtonX": 420,
    "routingButtonY": 255,
    "routingDiagonal": [309, 245, 444, 265],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

tom4RoomBParams = {
    "name": "Tom 4 Room B",
    "x": 820,
    "y": 674,
    "stateDiagonal": [157, 285, 158, 286],
    "volumeX": 458,
    "volumeY": 285,
    "volumeDiagonal": [478, 275, 528, 295],
    "panoramicX": 548,
    "panoramicY": 285,
    "panoramicDiagonal": [568, 275, 618, 295],
    "routingButtonX": 420,
    "routingButtonY": 285,
    "routingDiagonal": [309, 275, 444, 295],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

tom4SLRParams = {
    "name": "Tom 4 SLR",
    "x": 820,
    "y": 674,
    "stateDiagonal": [157, 315, 158, 316],
    "volumeX": 458,
    "volumeY": 315,
    "volumeDiagonal": [478, 305, 528, 325],
    "panoramicX": 548,
    "panoramicY": 315,
    "panoramicDiagonal": [568, 305, 618, 325],
    "routingButtonX": 420,
    "routingButtonY": 315,
    "routingDiagonal": [309, 305, 444, 325],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

hihatParams = {
    "name": "Hi-Hat",
    "x": 458,
    "y": 595,
    "stateDiagonal": [157, 195, 158, 196],
    "volumeX": 458,
    "volumeY": 195,
    "volumeDiagonal": [478, 185, 528, 205],
    "panoramicX": 548,
    "panoramicY": 195,
    "panoramicDiagonal": [568, 185, 618, 205],
    "routingButtonX": 420,
    "routingButtonY": 195,
    "routingDiagonal": [309, 185, 444, 205],
    "menuSize": 32,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

hihatOHParams = {
    "name": "Hi-Hat Over Head",
    "x": 458,
    "y": 595,
    "stateDiagonal": [],
    "volumeX": 458,
    "volumeY": 225,
    "volumeDiagonal": [478, 215, 528, 235],
    "panoramicX": 548,
    "panoramicY": 235,
    "panoramicDiagonal": [568, 215, 618, 235],
    "routingButtonX": 420,
    "routingButtonY": 225,
    "routingDiagonal": [309, 215, 444, 235],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

hihatRoomParams = {
    "name": "Hi-Hat Room",
    "x": 458,
    "y": 595,
    "stateDiagonal": [157, 255, 158, 256],
    "volumeX": 458,
    "volumeY": 255,
    "volumeDiagonal": [478, 245, 528, 265],
    "panoramicX": 548,
    "panoramicY": 255,
    "panoramicDiagonal": [568, 215, 618, 235],
    "routingButtonX": 420,
    "routingButtonY": 255,
    "routingDiagonal": [309, 245, 444, 265],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

hiHatRoomBParams = {
    "name": "Hi-Hat Room B",
    "x": 458,
    "y": 595,
    "stateDiagonal": [157, 285, 158, 286],
    "volumeX": 458,
    "volumeY": 285,
    "volumeDiagonal": [478, 275, 528, 295],
    "panoramicX": 548,
    "panoramicY": 285,
    "panoramicDiagonal": [568, 275, 618, 295],
    "routingButtonX": 420,
    "routingButtonY": 285,
    "routingDiagonal": [309, 275, 444, 295],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

cymbal1Params = {
    "name": "Crash 1 Over Head",
    "x": 568,
    "y": 465,
    "stateDiagonal": [157, 195, 158, 196],
    "volumeX": 458,
    "volumeY": 195,
    "volumeDiagonal": [478, 185, 528, 205],
    "panoramicX": 548,
    "panoramicY": 195,
    "panoramicDiagonal": [568, 185, 618, 205],
    "routingButtonX": 420,
    "routingButtonY": 195,
    "routingDiagonal": [309, 185, 444, 205],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

cymbal1RoomParams = {
    "name": "Crash 1 Room",
    "x": 568,
    "y": 465,
    "stateDiagonal": [],
    "volumeX": 458,
    "volumeY": 225,
    "volumeDiagonal": [478, 215, 528, 235],
    "panoramicX": 548,
    "panoramicY": 235,
    "panoramicDiagonal": [568, 215, 618, 235],
    "routingButtonX": 420,
    "routingButtonY": 225,
    "routingDiagonal": [309, 215, 444, 235],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

cymbal1RoomBParams = {
    "name": "Crash 1 Room B",
    "x": 568,
    "y": 465,
    "stateDiagonal": [157, 255, 158, 256],
    "volumeX": 458,
    "volumeY": 255,
    "volumeDiagonal": [478, 245, 528, 265],
    "panoramicX": 548,
    "panoramicY": 255,
    "panoramicDiagonal": [568, 215, 618, 235],
    "routingButtonX": 420,
    "routingButtonY": 255,
    "routingDiagonal": [309, 245, 444, 265],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

cymbal2Params = {
    "name": "Crash 2 Over Head",
    "x": 821,
    "y": 489,
    "stateDiagonal": [157, 195, 158, 196],
    "volumeX": 458,
    "volumeY": 195,
    "volumeDiagonal": [478, 185, 528, 205],
    "panoramicX": 548,
    "panoramicY": 195,
    "panoramicDiagonal": [568, 185, 618, 205],
    "routingButtonX": 420,
    "routingButtonY": 195,
    "routingDiagonal": [309, 185, 444, 205],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

cymbal2RoomParams = {
    "name": "Crash 2 Room",
    "x": 821,
    "y": 489,
    "stateDiagonal": [],
    "volumeX": 458,
    "volumeY": 225,
    "volumeDiagonal": [478, 215, 528, 235],
    "panoramicX": 548,
    "panoramicY": 235,
    "panoramicDiagonal": [568, 215, 618, 235],
    "routingButtonX": 420,
    "routingButtonY": 225,
    "routingDiagonal": [309, 215, 444, 235],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

cymbal2RoomBParams = {
    "name": "Crash 2 Room B",
    "x": 821,
    "y": 489,
    "stateDiagonal": [157, 255, 158, 256],
    "volumeX": 458,
    "volumeY": 255,
    "volumeDiagonal": [478, 245, 528, 265],
    "panoramicX": 548,
    "panoramicY": 255,
    "panoramicDiagonal": [568, 215, 618, 235],
    "routingButtonX": 420,
    "routingButtonY": 255,
    "routingDiagonal": [309, 245, 444, 265],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

cymbal3Params = {
    "name": "Splash Over Head",
    "x": 485,
    "y": 523,
    "stateDiagonal": [157, 195, 158, 196],
    "volumeX": 458,
    "volumeY": 195,
    "volumeDiagonal": [478, 185, 528, 205],
    "panoramicX": 548,
    "panoramicY": 195,
    "panoramicDiagonal": [568, 185, 618, 205],
    "routingButtonX": 420,
    "routingButtonY": 195,
    "routingDiagonal": [309, 185, 444, 205],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

cymbal3RoomParams = {
    "name": "Splash Room",
    "x": 485,
    "y": 523,
    "stateDiagonal": [],
    "volumeX": 458,
    "volumeY": 225,
    "volumeDiagonal": [478, 215, 528, 235],
    "panoramicX": 548,
    "panoramicY": 235,
    "panoramicDiagonal": [568, 215, 618, 235],
    "routingButtonX": 420,
    "routingButtonY": 225,
    "routingDiagonal": [309, 215, 444, 235],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

cymbal3RoomBParams = {
    "name": "Splash Room B",
    "x": 485,
    "y": 523,
    "stateDiagonal": [157, 255, 158, 256],
    "volumeX": 458,
    "volumeY": 255,
    "volumeDiagonal": [478, 245, 528, 265],
    "panoramicX": 548,
    "panoramicY": 255,
    "panoramicDiagonal": [568, 215, 618, 235],
    "routingButtonX": 420,
    "routingButtonY": 255,
    "routingDiagonal": [309, 245, 444, 265],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

cymbal4Params = {
    "name": "Ride",
    "x": 726,
    "y": 534,
    "stateDiagonal": [157, 195, 158, 196],
    "volumeX": 458,
    "volumeY": 195,
    "volumeDiagonal": [478, 185, 528, 205],
    "panoramicX": 548,
    "panoramicY": 195,
    "panoramicDiagonal": [568, 185, 618, 205],
    "routingButtonX": 420,
    "routingButtonY": 195,
    "routingDiagonal": [309, 185, 444, 205],
    "menuSize": 32,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

cymbal4OHParams = {
    "name": "Ride Over Head",
    "x": 726,
    "y": 534,
    "stateDiagonal": [],
    "volumeX": 458,
    "volumeY": 225,
    "volumeDiagonal": [478, 215, 528, 235],
    "panoramicX": 548,
    "panoramicY": 235,
    "panoramicDiagonal": [568, 215, 618, 235],
    "routingButtonX": 420,
    "routingButtonY": 225,
    "routingDiagonal": [309, 215, 444, 235],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

cymbal4RoomParams = {
    "name": "Ride Room",
    "x": 726,
    "y": 534,
    "stateDiagonal": [157, 255, 158, 256],
    "volumeX": 458,
    "volumeY": 255,
    "volumeDiagonal": [478, 245, 528, 265],
    "panoramicX": 548,
    "panoramicY": 255,
    "panoramicDiagonal": [568, 215, 618, 235],
    "routingButtonX": 420,
    "routingButtonY": 255,
    "routingDiagonal": [309, 245, 444, 265],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

cymbal4RoomBParams = {
    "name": "Ride Room B",
    "x": 726,
    "y": 534,
    "stateDiagonal": [157, 285, 158, 286],
    "volumeX": 458,
    "volumeY": 285,
    "volumeDiagonal": [478, 275, 528, 295],
    "panoramicX": 548,
    "panoramicY": 285,
    "panoramicDiagonal": [568, 275, 618, 295],
    "routingButtonX": 420,
    "routingButtonY": 285,
    "routingDiagonal": [309, 275, 444, 295],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

cymbal5Params = {
    "name": "Shina Over Head",
    "x": 909,
    "y": 575,
    "stateDiagonal": [157, 195, 158, 196],
    "volumeX": 458,
    "volumeY": 195,
    "volumeDiagonal": [478, 185, 528, 205],
    "panoramicX": 548,
    "panoramicY": 195,
    "panoramicDiagonal": [568, 185, 618, 205],
    "routingButtonX": 420,
    "routingButtonY": 195,
    "routingDiagonal": [309, 185, 444, 205],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

cymbal5RoomParams = {
    "name": "Shina Room",
    "x": 909,
    "y": 575,
    "stateDiagonal": [],
    "volumeX": 458,
    "volumeY": 225,
    "volumeDiagonal": [478, 215, 528, 235],
    "panoramicX": 548,
    "panoramicY": 235,
    "panoramicDiagonal": [568, 215, 618, 235],
    "routingButtonX": 420,
    "routingButtonY": 225,
    "routingDiagonal": [309, 215, 444, 235],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

cymbal5RoomBParams = {
    "name": "Shina Room B",
    "x": 909,
    "y": 575,
    "stateDiagonal": [157, 255, 158, 256],
    "volumeX": 458,
    "volumeY": 255,
    "volumeDiagonal": [478, 245, 528, 265],
    "panoramicX": 548,
    "panoramicY": 255,
    "panoramicDiagonal": [568, 215, 618, 235],
    "routingButtonX": 420,
    "routingButtonY": 255,
    "routingDiagonal": [309, 245, 444, 265],
    "menuSize": 36,
    "scroll": 75,
    "volume": setVolume,
    "panoramic": setPanoramic,
    "state": setState,
    "routing": setRouting
}

mixerObject = [
    kickInParams,
    kickOutParams,
    snareTopParams,
    snareBottomParams,
    snareRNGParams,
    tom1Params,
    tom2Params,
    tom3Params,
    tom4Params,
    hihatParams,
    cymbal4Params,
]

overHeadObject = [
    kickOHParams,
    snareOHParams,
    tom1OHParams,
    tom2OHParams,
    tom3OHParams,
    tom4OHParams,
    hihatOHParams,
    cymbal1Params,
    cymbal2Params,
    cymbal3Params,
    cymbal4OHParams,
    cymbal5Params,
]

roomObject = [
    kickRoomParams,
    snareRoomParams,
    tom1RoomParams,
    tom2RoomParams,
    tom3RoomParams,
    tom4RoomParams,
    hihatRoomParams,
    cymbal1RoomParams,
    cymbal2RoomParams,
    cymbal3RoomParams,
    cymbal4RoomParams,
    cymbal5RoomParams,
]

roomBObject = [
    kickRoomBParams,
    snareRoomBParams,
    tom1RoomBParams,
    tom2RoomBParams,
    tom3RoomBParams,
    tom4RoomBParams,
    hiHatRoomBParams,
    cymbal1RoomBParams,
    cymbal2RoomBParams,
    cymbal3RoomBParams,
    cymbal4RoomBParams,
    cymbal5RoomBParams,
    ]

SLRObject = [
    kickSLRParams,
    tom1SLRParams,
    tom2SLRParams,
    tom3SLRParams,
    tom4SLRParams,
]
mixerTypeList = [
    {"name": "Pieces", "object": mixerObject},
    {"name": "Over Heads", "object": overHeadObject},
    {"name": "Room", "object": roomObject},
    {"name": "Room B", "object": roomBObject},
    {"name": "SLR", "object": SLRObject},
]
