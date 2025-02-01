import subprocess, os, api, ui
from scriptHandler import script
import globalPluginHandler


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    @script(gesture="kb:NVDA+shift+u")
    def script_get_reaper_upgrade(self, gesture):
        app = api.getForegroundObject ()

        if ' - REAPER v' in app.name:
            ui.message("Update Error : You must quit Reaper befor raise the update")
        else:
            ui.message("Reaper update")
            user_folder = os.path.expanduser('~')
            reaper_update = open(user_folder + "\\AppData\\Roaming\\nvda\\addons\\LBL\\globalPlugins\\reaper-update.txt", 'w')
            si = subprocess.STARTUPINFO()
            si.dwFlags = subprocess.STARTF_USESHOWWINDOW
            si.wShowWindow = subprocess.SW_HIDE
            subprocess.call("winget upgrade reaper", startupinfo=si, stdout=reaper_update)
            reaper_update.close()
            reaper_update = open(user_folder + "\\AppData\\Roaming\\nvda\\addons\\LBL\\globalPlugins\\reaper-update.txt", 'r')
            lines = reaper_update.readlines()
            ui.message(lines[-1]
                .replace('Ã©','é')
                .replace('Ã ', 'à')
                .replace('.\n', ''))
            reaper_update.close()
            os.remove(user_folder + "\\AppData\\Roaming\\nvda\\addons\\LBL\\globalPlugins\\reaper-update.txt")

