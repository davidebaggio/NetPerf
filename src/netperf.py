from linux import main as linuxmain
from windows import main as windowsmain
import os
import numpy as np
import matplotlib.pyplot as plt


# detect operating system
def detect_os():
    if os.name == "nt":
        return "windows"
    elif os.name == "posix":
        return "linux"
    else:
        return "unknown"

# running network performance


if __name__ == "__main__":
    os = detect_os()
    if os == "windows":
        windowsmain()
    elif os == "linux":
        linuxmain()
    else:
        print("Unknown operating system")
        exit(1)
