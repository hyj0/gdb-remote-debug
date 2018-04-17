import os
import sys
from PyInstaller import __main__ as PyInstallerMain

if __name__ == "__main__":
    configPath=os.path.join(os.path.dirname(sys.argv[0]), "config.ini")
    configPlacePyFile = os.path.join(os.path.dirname(sys.argv[0]), "config_place.py")
    f = open(configPlacePyFile, "w")
    f.write("configFilePath=\"" + configPath  + "\"")
    f.close()

    sys.argv = [sys.argv[0], "--onefile", "gdb.py"]
    PyInstallerMain.run()

    sys.argv[2] = "WinProcessListHelper.py"
    PyInstallerMain.run()
