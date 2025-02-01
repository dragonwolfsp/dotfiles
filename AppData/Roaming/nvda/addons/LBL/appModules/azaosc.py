# Import des modules NVDA
import appModuleHandler
import ui
import api
from scriptHandler import script
import tones
import keyboardHandler
import controlTypes
import gui
import wx

# Import des modules LBL
from .lbl.api.navobject import NavObject

# Import des modules AZOSC
from .lbl.azaosc.zoneslist import params

class AppModule(appModuleHandler.AppModule):
    paramList = NavObject(params)
    pw_activated = False
    meter = None


    @script(gesture="kb:NVDA+SHIFT+rightarrow")
    def script_go_to_next_param(self, gesture):
        ui.message(self.paramList.getNextObject())


    @script(gesture="kb:NVDA+SHIFT+leftarrow")
    def script_go_to_previous_param(self, gesture):
        ui.message(self.paramList.getPreviousObject())

    @script(gesture="kb:SHIFT+CONTROL+W")
    def script_toggle_pw(self, gesture):
        if self.pw_activated == False:
            obj_test = api.getFocusObject()

            if "Meter" not in obj_test.name:
                ui.message("It is not a meter")
                return
            self.meter = api.getFocusObject()
            ui.message(f"{self.meter.name} traking")
            self.pw_activated = True
        else:
            self.meter = None
            ui.message("Traking off")
            self.pw_activated = False


    @script(gesture="kb:downarrow")
    def script_press_downarrow(self, gesture):
        obj = api.getFocusObject()
        keyboardHandler.KeyboardInputGesture.fromName("downarrow").send()
        ui.message(obj.value)


    @script(gesture="kb:uparrow")
    def script_press_uparrow(self, gesture):
        obj = api.getFocusObject()
        keyboardHandler.KeyboardInputGesture.fromName("uparrow").send()
        ui.message(obj.value)    


    @script(gesture="kb:leftarrow")
    def script_press_leftarrow(self, gesture):
        obj = api.getFocusObject()
        keyboardHandler.KeyboardInputGesture.fromName("leftarrow").send()
        ui.message(obj.value)


    @script(gesture="kb:rightarrow")
    def script_press_rightarrow(self, gesture):
        obj = api.getFocusObject()
        keyboardHandler.KeyboardInputGesture.fromName("rightarrow").send()
        ui.message(obj.value)


    @script(gesture="kb:pageup")
    def script_press_pageup(self, gesture):
        obj = api.getFocusObject()
        keyboardHandler.KeyboardInputGesture.fromName("pageup").send()
        ui.message(obj.value)


    @script(gesture="kb:pagedown")
    def script_press_pagedown(self, gesture):
        obj = api.getFocusObject()
        keyboardHandler.KeyboardInputGesture.fromName("pagedown").send()
        ui.message(obj.value)


    @script(gesture="kb:home")
    def script_press_home(self, gesture):
        obj = api.getFocusObject()

        if obj.role == controlTypes.Role.SLIDER:
            key = "end"
        else:
            key = "home"
        keyboardHandler.KeyboardInputGesture.fromName(key).send()
        ui.message(obj.value)


    @script(gesture="kb:end")
    def script_press_end(self, gesture):
        obj = api.getFocusObject()

        if obj.role == controlTypes.Role.SLIDER:
            key = "home"
        else:
            key = "end"
        keyboardHandler.KeyboardInputGesture.fromName(key).send()
        ui.message(obj.value)


    @script(gesture="kb:space")
    def script_press_space(self, gesture):
        obj = api.getFocusObject()
        keyboardHandler.KeyboardInputGesture.fromName("space").send()
        ui.message(obj.value)
    
    
    @script(gesture="kb:NVDA+a")
    def script_set_configuration(self, gesture):
        pass


    def event_valueChange(self, obj, nextHandler):
        if self.pw_activated == True and self.meter != None:
            intValue = int(self.meter.value[0 : -2])
            if intValue > -19 and intValue < -3:
                tones.beep(1000, 50)
            if intValue  > -4:
                tones.beep(2000, 100)
        nextHangler()
