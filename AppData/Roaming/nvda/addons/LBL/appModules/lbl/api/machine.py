from ctypes import *
from ctypes.wintypes import *
import os

machine_dir = os.path.dirname(__file__)
dll_path = os.path.join(machine_dir, "battery.dll")
battery = WinDLL(dll_path)

def get_machine_type():
    get_type_machine = battery.GetTypeMachine
    get_type_machine.restype = c_wchar_p
    res = get_type_machine()
    return res
#
