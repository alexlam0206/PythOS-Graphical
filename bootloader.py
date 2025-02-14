import os
import sys

with open("PythOS/boot/boot_selection.txt", "r") as boot_decide:
    boot_decide = boot_decide.read()
    if boot_decide == "1":
        os.system("python3 main2.py")
    elif boot_decide == "2":
        os.system("loadup_terminal.bat")
sys.exit()
