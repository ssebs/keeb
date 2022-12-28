#!/usr/bin/env python3
# notify.py - Notify user of keyboard mode switches

import time
import signal
import sys
import threading

import serial
import serial.tools.list_ports
from playsound import playsound

from util import switchMode, MACRO_ITEMS
from macrodisplay import MacroDisplay
from tkinter import Tk

DEBUG = True
SECOND_MONITOR = False

ICON_PATH = './client/res/bell.ico'
SFX_PATH = './client/res/snap.mp3'

def main():
    print("Client for macro pad")
    signal.signal(signal.SIGINT, signal.default_int_handler)
    # TODO: Find correct port automatically
    serial_port = load_port("COM7")
    arduino = serial.Serial(port=serial_port, baudrate=9600,  timeout=1.2)
    if arduino is None:
        print("Failed to mount COM7")

    global root
    root = Tk()
    macro_display = MacroDisplay(root, "MODE")
    

    root.protocol("WM_DELETE_WINDOW", handle_close)
    root.iconbitmap(ICON_PATH)

    posX = None
    posY = None


    # GUI stuff
    if SECOND_MONITOR:
        posX = root.winfo_screenwidth() + int(root.winfo_screenwidth() / 2)
        posY = root.winfo_screenheight() - int(root.winfo_screenheight() / 2)
    else:
        posX = int(root.winfo_screenwidth() / 2)
        posY = int(root.winfo_screenheight() / 2)
    root.geometry(f"456x300+{posX}+{posY}")

    global thread1 
    thread1 = threading.Thread(target=main_loop, args=(arduino, root, macro_display))
    thread1.daemon = True
    thread1.start()

    root.mainloop()


def main_loop(arduino, root, macro_display):
    while True:
        data = str(arduino.readline().decode())
        if data != "" and DEBUG:
            print(data)

        if data.startswith("key:"):
            keyPressed = int(data.split(":")[1].strip())
            print(f"Key pressed: {keyPressed}")

        if data.startswith("secmode:"):
            mode = int(data.split(":")[1].strip())
            # print(switchMode(mode).name)
            macro_display.update_mode(switchMode(mode).name, is_auto=True)
        if data.startswith("mode:"):
            mode = int(data.split(":")[1].strip())
            # print(switchMode(mode).name)
            macro_display.update_mode(switchMode(mode).name)
            playsound(SFX_PATH, False)

        if data.startswith("log:"):
            print(data)


def load_port(name: str) -> str:
    ports = list(serial.tools.list_ports.comports())
    if DEBUG:
        print("Serial Ports:")
    for p in ports:
        if DEBUG:
            print(f"{p.name} - {p.description}")
        if p.name == name:
            return p.name
    return None


def handle_close():
    if thread1 is not None:
        root.destroy()
        thread1.join()
        exit(0)
    else:
        print("thread is none")
        root.destroy()
        exit(0)
    # stop thread1

if __name__ == "__main__":
    main()
