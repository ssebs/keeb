#!/usr/bin/env python3
# notify.py - Notify user of keyboard mode switches

import time
import signal
import sys

import serial
import serial.tools.list_ports
from win10toast import ToastNotifier

from util import switchMode, MACRO_ITEMS
from macrodisplay import MacroDisplay
from tkinter import Tk

DEBUG = True
SECOND_MONITOR = True


def main():
    print("Client for macro pad")
    signal.signal(signal.SIGINT, signal.default_int_handler)
    serial_port = load_port("COM7")
    arduino = serial.Serial(port=serial_port, baudrate=9600,  timeout=1.2)
    toast = ToastNotifier()

    root = Tk()
    macro_display = MacroDisplay(root)
    posX = None
    posY = None

    if arduino is None:
        print("Failed to mount COM7")

    # GUI stuff
    if SECOND_MONITOR:
        posX = root.winfo_screenwidth() + int(root.winfo_screenwidth() / 2)
        posY = root.winfo_screenheight() - int(root.winfo_screenheight() / 2)
    else:
        posX = int(root.winfo_screenwidth() / 2)
        posY = int(root.winfo_screenheight() / 2)
    root.geometry(f"256x256+{posX}+{posY}")
    
    root.mainloop()

    while True:
        data = str(arduino.readline().decode())
        if data != "" and DEBUG:
            print(data)
        if data.startswith("key:"):
            keyPressed = int(data.split(":")[1].strip())
            print(f"Key pressed: {keyPressed}")
        if data.startswith("mode:"):
            # main()
            mode = int(data.split(":")[1].strip())
            print(switchMode(mode).name)
            toast.show_toast("Keyboard mode:", switchMode(
                mode).name, duration=2, icon_path='')
        if data.startswith("log:"):
            print(data)


def load_port(name: str) -> str:
    ports = list(serial.tools.list_ports.comports())
    if DEBUG:
        print("Serial Ports:")
    for p in ports:
        if DEBUG:
            print(p.name)
        if p.name == name:
            return p.name
    return None


if __name__ == "__main__":
    main()
