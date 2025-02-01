import ui
from .mouse import Mouse

# Classe regroupant les fonctions permettant le déplacement dans une arboressence LBL
class NavObject:
    mouse = Mouse()

    def __init__(self, list, paramsPosition = 0):
        self.list = list
        self.i = 0
        self.paramsPosition = paramsPosition
        self.defaultParamsPosition = paramsPosition
        self.object = self.list[0]

    def getObject(self, mouse = None):
        if mouse == "move":
            self.mouse.moveCursor(self.object["x"], self.object["y"])
        elif mouse == "move_and_click":
            self.mouse.moveAndLeftClick(self.object["x"], self.object["y"])
        elif mouse == "absolut_move":
            self.mouse.absolutMoveCursor(self.object["x"], self.object["y"])
        elif mouse == "absolut_move_and_click":
            self.mouse.absolutMoveAndLeftClick(self.object["x"], self.object["y"])
        return self.object

    def getNextObject(self, mouse = None):
        if (self.i + 1) < len(self.list):
            self.i += 1
        else:
            self.i = 0
        self.object = self.list[self.i]

        if mouse == "move":
            self.mouse.moveCursor(self.object["x"], self.object["y"])
        elif mouse == "move_and_click":
            self.mouse.moveAndLeftClick(self.object["x"], self.object["y"])
        elif mouse == "absolut_move":
            self.mouse.absolutMoveCursor(self.object["x"], self.object["y"])
        elif mouse == "absolut_move_and_click":
            self.mouse.absolutMoveAndLeftClick(self.object["x"], self.object["y"])


        return self.object

    def getPreviousObject(self, mouse = None):
        if self.i == -1:
            self.i = 0
            self.object = self.list[self.i]

        if self.i == 0:
            self.i = len(self.list) - 1
        else:
            self.i -= 1
        self.object = self.list[self.i]

        if mouse == "move":
            self.mouse.moveCursor(self.object["x"], self.object["y"])
        elif mouse == "absolut_move":
            self.mouse.absolutMoveCursor(self.object["x"], self.object["y"])
        elif mouse == "absolut_move_and_click":
            self.mouse.absolutMoveAndLeftClick(self.object["x"], self.object["y"])
        elif mouse == "move_and_click":
            self.mouse.moveAndLeftClick(self.object["x"], self.object["y"])

        return self.object

    def resetObject(self):
        self.i = 0
        self.object = self.list[0]

    def getSubObject(self):
        index = 0
        
        for it in self.object.items():
            if index == self.paramsPosition:
                return it
            index += 1

    def getNextSubObject(self):
        if self.paramsPosition < (len(self.object) - 1):
            self.paramsPosition += 1
        else:
            self.paramsPosition = self.defaultParamsPosition
        return self.getSubObject()

    def getPreviousSubObject(self):
        if self.paramsPosition == self.defaultParamsPosition:
            self.paramsPosition = len(self.object) - 1
        else:
            self.paramsPosition -= 1
        return self.getSubObject()

    def goToObjectByName(self, name):
        self.resetObject()

        for o in self.list:
            if o == name:
                return self.getObject()
            self.getNextObject()
        return ""
