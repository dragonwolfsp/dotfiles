# Import des modules NVDA
import ui
from NVDAObjects.IAccessible import IAccessible
from scriptHandler import script

# Import des modules LBL
from ..api.navobject import NavObject
from ..api.ocr import LBLOCR
from ..api.mouse import Mouse

# Import des module propres à GTune
from .itemlist import itemList
from .tunedictionnary import tuneDictionnary

class GTune(IAccessible):
    name = "LBL_GTune"
    itemlist = NavObject(itemList)
    mouse = Mouse()

    @script(gestures=["kb:leftarrow", "kb:shift+tab"])
    def script_previousItem(self, gesture):
        """
            Aller à l'objet précédent de l'interface
        """

        ui.message(self.itemlist.getPreviousObject()["name"])

        if self.itemlist.getObject()['name'] == 'Reference':
            ui.message(LBLOCR.getText([230, 35, 280, 50]))
        elif self.itemlist.getObject()['name'] == 'Tune':
            ui.message(self.getTune())

    @script(gestures=["kb:rightarrow", "kb:tab"])
    def script_nextItem(self, gesture):
        """
            Aller à l'objet suivant de l'interface
        """
        ui.message(self.itemlist.getNextObject()["name"])

        if self.itemlist.getObject()['name'] == 'Reference':
            ui.message(LBLOCR.getText([230, 35, 280, 50]))
        elif self.itemlist.getObject()['name'] == 'Tune':
            ui.message(self.getTune())

    @script(gesture="kb:enter")
    def script_defaultAction(self, gesture):
        """
            Déclanchement de l'action par défaut de chaque item.
            Reference : Ouverture de la zone d'édition de la fréquence de référence.
            Tune : énonciation de la note, et de sa justesse.
        """

        item = self.itemlist.getObject()
        
        if item["name"] == "Reference":
            self.mouse.moveAndLeftClick(240, 40)
        elif item["name"] == "Tune":
            ui.message(self.getTune())
    
    def getTune(self):
        """
            Obtention de la note et de sa justesse, puis corrections des incoérences générées par l'OCR
        """
        tune = LBLOCR.getText([160, 210, 280, 250])
        tune = LBLOCR.getCorrection(tune, tuneDictionnary)
        tune = tune.replace('i', '')
        tune = tune.replace('l', '')
        tune = tune.replace('%', '')
        tune = tune.replace('|', '')
        tune = tune.replace('_', '')
        tune = tune.replace('k', '')
        tune = tune.replace('{', '')
        tune = tune.replace('}', '')
        tune = tune.replace(')', '')
        tune = tune.replace('-', ' minus ')
        tune = tune.replace('+', ' plus ')
        tune = tune .replace('#', ' sharp')
        tune = tune.replace('o', '0')
        tune = tune.replace('cs', 'g')
        tune = tune.replace('<s', 'g')
        tune = tune.replace('ãž', '')
        tune = tune.replace(':â€º', 'd')
        tune = tune.replace('câ€º', 'd')

        if "0" in tune:
            return "Tuned"
        return tune
