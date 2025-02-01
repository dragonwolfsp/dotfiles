import ui
import os
import sys
import config
import tempfile
import subprocess
import api

PLUGIN_DIR = os.path.dirname(__file__)
TESSERACT_EXE = os.path.join(PLUGIN_DIR, "tesseract", "tesseract.exe")
sys.path.append(PLUGIN_DIR)

from .PIL import Image, ImageGrab, ImageOps
from scriptHandler import script

class LBLOCR:
    IMAGE_RESIZE_FACTOR = 5

    def getText(diagonal = []):
        file_path_save = os.path.join(PLUGIN_DIR, 'ocr.png')
        
        (winLeft, winTop) = LBLOCR.getWindow()

        img = ImageGrab.grab(bbox=(winLeft + diagonal[0], winTop + diagonal[1], winLeft + diagonal[2], winTop + diagonal[3]))
        img.save(file_path_save, dpi=(300, 300))
        img = img.convert('L')
        img = ImageOps.invert(img)

        img = img.resize(tuple(LBLOCR.IMAGE_RESIZE_FACTOR * x for x in img.size), Image.BICUBIC)
        baseFile = os.path.join(tempfile.gettempdir(), "nvda_ocr")

        imgFile = baseFile + ".bmp"
        img.save(imgFile)
     
        # Hide the Tesseract window.
        si = subprocess.STARTUPINFO()
        si.dwFlags = subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = subprocess.SW_HIDE
        subprocess.check_call((TESSERACT_EXE, imgFile, baseFile, "-l", "fra", "ocr"), startupinfo=si)

        ocrFile = baseFile + '.txt'

        return open(ocrFile).read()

    def getColor(diagonal = [], colorX = 1, colorY = 1):
        obj = api.getFocusObject()
        winLeft = obj.location[0]
        winTop = obj.location[1]

        (winLeft, winTop) = LBLOCR.getWindow()
        img = ImageGrab.grab(bbox=(winLeft + diagonal[0], winTop + diagonal[1], winLeft + diagonal[2], winTop + diagonal[3]))
        return LBLOCR.rgb2hex(img.getpixel((colorX, colorY)))

    def getCorrection(world, list):
        world = world.replace(' ', '').replace('\n', '').lower()

        for l in list:
            if world in l["list"]:
                return l["correction"]
        return world

    def getWindow():
        obj = api.getFocusObject()
        winLeft = obj.location[0]
        winTop = obj.location[1]

        return winLeft,winTop
    
    def rgb2hex(rgb):
        (r, g, b) = rgb
        
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)

