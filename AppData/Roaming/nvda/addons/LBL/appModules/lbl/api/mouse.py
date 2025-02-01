import api
import winUser
import time

class Mouse:
    def getLeftMargin(self):
        return api.getFocusObject().location[0]

    def getTopMargin(self):
        return api.getFocusObject().location[1]

    def moveCursor(self, x, y):
        """
            Déplacement du curseur de souris aux coordonnées x, y
        """

        x = x + self.getLeftMargin()
        y = y + self.getTopMargin()
        winUser.setCursorPos(x, y)

    def absolutMoveCursor(self, x, y):
        """
            Déplacement du curseur de souris aux coordonnées x, y
        """

        winUser.setCursorPos(x, y)
    
    def leftClick(self):
        """
            Déclanchement d'un click gauche
        """

        winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN, 0, 0, None, None)
        winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP, 0, 0, None, None)

    def doubleClick(self):
        self.leftClick()
        time.sleep(0.05)
        self.leftClick()

    def moveAndLeftClick(self, x, y):
        """
            Déplacement du curseur de souris au coordonnées x, y; et déclanchement d'un click gauche
        """

        self.moveCursor(x, y)
        self.leftClick()
    
    def absolutMoveAndLeftClick(self, x, y):
        """
            Déplacement du curseur de souris au coordonnées x, y; et déclanchement d'un click gauche
        """

        self.absolutMoveCursor(x, y)
        self.leftClick()

    def dragVertical(self, x, y, step):
        self.moveCursor(x, y)

        winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN, 0, 0, None, None)
        self.moveCursor(x, y - step)
        time.sleep(0.05)
        winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP, 0, 0, None, None)

    def moveAndScroll(self, x, y, step):
        self.moveCursor(x, y)
        winUser.mouse_event(winUser.MOUSEEVENTF_WHEEL, 0, 0, step, None)
        time.sleep(0.01)
        return

