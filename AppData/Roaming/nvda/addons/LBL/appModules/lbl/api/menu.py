import ui
from .mouse import Mouse
from .ocr import LBLOCR

class Menu:
    mouse = Mouse()
    diagonal = []
    index = 0

    def openMenu(self, x, y):
        self.mouse.moveAndLeftClick(x, y)

    def getNbItems(self, colorX, colorY, colorCodes = [], diagonal = []):
        nbItems = 0
        self.diagonal = diagonal

        diagonalHeight = diagonal[3] - diagonal[1]
        color = LBLOCR.getColor(diagonal, colorX, colorY)

        while color in colorCodes:
            diagonal = [diagonal[0], diagonal[1] + diagonalHeight, diagonal[2], diagonal[3] + diagonalHeight]
            color = LBLOCR.getColor(diagonal, colorX, colorY)
            if (color not in colorCodes):
                break
            nbItems += 1

        return nbItems

    def getItem(self, index):
        indexDiff = self.index - index
        diagonalHeight = self.diagonal[3] - self.diagonal[1]
        diagonalDiff = indexDiff * diagonalHeight
        self.index -= index
        self.diagonal = [self.diagonal[0], self.diagonal[1] + diagonalDiff, self.diagonal[2], self.diagonal[3] + diagonalDiff]

    def getPreviousItem(self):
        diagonalHeight = self.diagonal[3] - self.diagonal[1]
        self.index -= 1
        self.diagonal = [self.diagonal[0], self.diagonal[1] - diagonalHeight, self.diagonal[2], self.diagonal[3] - diagonalHeight]
        ui.message(LBLOCR.getText(self.diagonal))

    def getNextItem(self):
        diagonalHeight = self.diagonal[3] - self.diagonal[1]
        self.index += 1
        self.diagonal = [self.diagonal[0], self.diagonal[1] + diagonalHeight, self.diagonal[2], self.diagonal[3] + diagonalHeight]
        ui.message(LBLOCR.getText(self.diagonal))