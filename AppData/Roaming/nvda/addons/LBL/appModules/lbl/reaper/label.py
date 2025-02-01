import ui
import api
import controlTypes

def setLabels(obj):
    """
    On étiquette les composants d'interface qui ne le sont pas
    """

    if obj.windowControlID == 1426:
        label = "Activer l'FX"
    elif obj.windowControlID == 1192 and obj.name == '...':
        label = "Commentaire"
    elif obj.windowControlID == 1087:
        label = "Sortie matérielle"
    else:
        return
    ui.message(label)
