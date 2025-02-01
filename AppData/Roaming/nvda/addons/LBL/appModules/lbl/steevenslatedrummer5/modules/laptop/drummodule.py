from ....api.mouse import Mouse
from ....api.ocr import LBLOCR
import time

mouse = Mouse()

def setVolume(arrow, x = 0, y = 0):
    """
        Ajustement du volume de la pièce
    """

    if arrow == "right":
        mouse.moveAndScroll(332, 77, 50)
    elif arrow == "left":
        mouse.moveAndScroll(332, 77, -50)
    mouse.moveAndLeftClick(x, y)

def setPresence(arrow, x, y):
    """
        Ajustement de la présence de la pièce
    """

    if arrow == "right":
        mouse.moveAndScroll(700, 188, 34)
    elif arrow == "left":
        mouse.moveAndScroll(700, 188, -34)
    mouse.moveAndLeftClick(x, y)

def setTune(arrow, x = 0, y = 0):
    """
        Ajustement de l'accord de la pièce
    """

    if arrow == "right":
        mouse.moveAndScroll(332, 110, 50)
    elif arrow == "left":
        mouse.moveAndScroll(332, 110, -50)
    mouse.moveAndLeftClick(x, y)

# Dictionnaire regroupant les paramètres de la grosse caisse
kickParams = {
    "name": "Kick",
    "x": 641,
    "y": 670,
    "volume": setVolume,
    "presence": setPresence,
    "tune": setTune,
}

# Dictionnaire regroupant les paramètres de la caisse claire
snareParams = {
    "name": "Snare",
    "x": 547 ,
    "y": 613,
    "volume": setVolume,
    "presence": setPresence,
    "tune": setTune,
}
  
# Dictionnaire regroupant les paramètres du tom 1
tom1Params = {
    "name": "Tom 1",
    "x": 550,
    "y": 544,
    "volume": setVolume,
    "presence": setPresence,
    "tune": setTune,
}

# Dictionnaire regroupant les paramètres du tom 2
tom2Params = {
    "name": "Tom 2",
    "x": 626,
    "y": 526,
    "volume": setVolume,
    "presence": setPresence,
    "tune": setTune,
}

# Dictionnaire regroupant les paramètres du tom 3
tom3Params = {
    "name": "Tom 3",
    "x": 758,
    "y": 610,
    "volume": setVolume,
    "presence": setPresence,
    "tune": setTune,
}

# Dictionnaire regroupant les paramètres du tom 4
tom4Params = {
    "name": "Tom 4",
    "x": 820,
    "y": 674,
    "volume": setVolume,
    "presence": setPresence,
    "tune": setTune,
}

# Dictionnaire regroupant les paramètres du charley
hihatParams = {
    "name": "Hi-Hat",
    "x": 458,
    "y": 595,
    "volume": setVolume,
    "presence": setPresence,
    "tune": setTune,
}

# Dictionnaire regroupant les paramètres de la cimbale 1
cymbal1Params = {
    "name": "Crash 1",
    "x": 568,
    "y": 465,
    "volume": setVolume,
    "presence": setPresence,
    "tune": setTune,
}

# Dictionnaire regroupant les paramètres de la cimbale 2
cymbal2Params = {
    "name": "Crash 2",
    "x": 821,
    "y": 489,
    "volume": setVolume,
    "presence": setPresence,
    "tune": setTune,
}

# Dictionnaire regroupant les paramètres de la cimbale 3
cymbal3Params = {
    "name": "Splash",
    "x": 485,
    "y": 523,
    "volume": setVolume,
    "presence": setPresence,
    "tune": setTune,
}

# Dictionnaire regroupant les paramètres de la cimbale 4
cymbal4Params = {
    "name": "Ride",
    "x": 726,
    "y": 534,
    "volume": setVolume,
    "presence": setPresence,
    "tune": setTune,
}

# Dictionnaire regroupant les paramètres de la cimbale 5
cymbal5Params = {
    "name": "Shina",
    "x": 909,
    "y": 575,
    "volume": setVolume,
    "presence": setPresence,
    "tune": setTune,
}

# Liste regroupant les dictionnaires correspondant aux paramètres de chaque élément de la batterie
drumObject = [
    kickParams,
    snareParams,
    tom1Params,
    tom2Params,
    tom3Params,
    tom4Params,
    hihatParams,
    cymbal1Params,
    cymbal2Params,
    cymbal3Params,
    cymbal4Params,
    cymbal5Params,
]
