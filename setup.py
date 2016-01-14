# -*- coding: utf-8- -*-
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
                    "packages": ["os"], 
                    # "excludes": ["tkinter"],
                    "compressed": True
                    }

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"
	
	

setup(  name = "Berater",
        version = "0.6",
        description = u"Abrechnungsprogramm für Berater",
        options = {"build_exe": build_exe_options},
        executables = [Executable("berater.py", 
                                   base=base,
                                   shortcutName="Berater - Abrechnungsprogramm",
                                   shortcutDir="StartMenuFolder")
                       ]
        )
