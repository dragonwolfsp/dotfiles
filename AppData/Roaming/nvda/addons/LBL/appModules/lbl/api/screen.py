import time
from . import pyautogui
import ui

def locate_and_click(img, xOffset = 0, yOffset = 0, xCleanMouse = 0, yCleanMouse = 0):
    coords = pyautogui.locateCenterOnScreen(img)
    if coords == None:
        ui.message("Image Introuvable")
    else:
        pyautogui.click(coords[0] + xOffset, coords[1] + yOffset)
        pyautogui.move(xCleanMouse, yCleanMouse)
#

