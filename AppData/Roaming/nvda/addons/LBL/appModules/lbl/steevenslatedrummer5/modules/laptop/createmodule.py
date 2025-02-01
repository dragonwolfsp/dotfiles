import os
import ui
import time
from ....api.ocr import LBLOCR
from ....api.mouse import Mouse

mouse = Mouse()

col1 = {
    "position": 1,
    "diagonal": [132, 50, 407, 72],
}

col2 = {
    "position": 1,
    "diagonal": [412, 50, 672, 72]
}

col3 = {
    "position": 1,
    "diagonal": [677, 50, 942, 72],
}

def resetCol1():
    col1["position"] = 1
    col1["diagonal"] = [132, 50, 407, 72]

def resetCol2():
    col2["position"] = 1
    col2["diagonal"] = [412, 50, 672, 72]

def resetCol3():
    col3["position"] = 1
    col3["diagonal"] = [677, 50, 942, 72]

def resetColumns():
    resetCol1()
    resetCol2()
    resetCol3()

def getLibraryNumber():
    return len(os.listdir("c:/Program Files/VSTPlugins/SSD5Library/DrumKitPresets"))

def getCategoryNumber():
    lib = os.listdir("c:/Program Files/VSTPlugins/SSD5Library/DrumKitPresets/")[col1["position"] - 1]
    path = "c:/Program Files/VSTPlugins/SSD5Library/DrumKitPresets/" + lib

    return len(os.listdir(path))

def getPresetNumber():
    lib = os.listdir("c:/Program Files/VSTPlugins/SSD5Library/DrumKitPresets/")[col1["position"] - 1]
    category = os.listdir("c:/Program Files/VSTPlugins/SSD5Library/DrumKitPresets/" + lib)[col2["position"] - 1]
    path = "c:/Program Files/VSTPlugins/SSD5Library/DrumKitPresets/" + lib + "/" + category

    return len(os.listdir(path))

def getLibrary(key = None, libraryNumber = 0):
    if key == "down":
        if col1["position"] < libraryNumber:
            col1["position"] += 1
            col1["diagonal"][1] += 22
            col1["diagonal"][3] += 22
    elif key == "up":
        if col1["position"] > 1:
            col1["position"] -= 1
            col1["diagonal"][1] -= 22
            col1["diagonal"][3] -= 22
    if key == "enter":
        ui.message("Kick selection")
    mouse.moveAndLeftClick(col1["diagonal"][0] + 5, col1["diagonal"][1] + 5)

    return LBLOCR.getText(col1["diagonal"])

def getCategory(key = None, categoryNumber = 0):
    if key == "down":
        if col2["position"] < categoryNumber:
            col2["position"] += 1
            col2["diagonal"][1] += 22
            col2["diagonal"][3] += 22
    elif key == "up":
        if col2["position"] > 1:
            col2["position"] -= 1
            col2["diagonal"][1] -= 22
            col2["diagonal"][3] -= 22
        
    mouse.moveAndLeftClick(col2["diagonal"][0] + 5, col2["diagonal"][1] + 5)

    return LBLOCR.getText(col2["diagonal"])

def getPreset(key = None, presetNumber = 0):
    if key == "down":
        if col3["position"] < presetNumber:
            col3["position"] += 1
            col3["diagonal"][1] += 22
            col3["diagonal"][3] += 22
    elif key == "up":
        if col3["position"] > 1:
            col3["position"] -= 1
            col3["diagonal"][1] -= 22
            col3["diagonal"][3] -= 22
        
    mouse.moveAndLeftClick(col3["diagonal"][0] + 5, col3["diagonal"][1] + 5)

    return LBLOCR.getText(col3["diagonal"])

# Dictionnaire contenant les paramètres du tableau Kits
kitsParams = {
    "name": "Kits",
    "libraryNumber": getLibraryNumber,
    "library": getLibrary,
    "categoryNumber": getCategoryNumber,
    "category": getCategory,
    "presetNumber": getPresetNumber,
    "preset": getPreset,
}

# Dictionnaire contenant les paramètres du tableau Instruments
instrumentsParams = {
    "name": "Instruments",
    "libraryNumber": getLibraryNumber,
    "library": getLibrary,
}

# Liste des dictionnaires correspondant aux parties de l'onglet Create
createObject = [
    kitsParams,
]
