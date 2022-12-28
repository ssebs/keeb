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

DEBUG = False
SECOND_MONITOR = False
ICON_PATH = './client/res/bell.ico'
SFX_PATH = './client/res/snap.mp3'
SERIAL_QRY = "USB Serial Device"


def main():
    """
    Main function
    TODO: Make this OOP instead of using global vars and constants
    """
    if DEBUG:
        print("Client for macro pad")
    
    try:
        arduino = init_arduino()
        macro_display = init_gui() # sets global root, returns MacroDisplay
    except Exception as e:
        print(e)
        exit(1)

    # Setup Serial comm thread
    global thread1 
    thread1 = threading.Thread(target=main_loop, args=(arduino, root, macro_display), daemon=True)
    thread1.start()
    
    # For the close icon in the GUI, stop the thread too
    global do_close
    do_close = False

    # Start GUI thread (main)
    root.mainloop()
# end main

def init_arduino() -> serial.Serial:
    """
    Initialize serial COM port and return it. Uses SERIAL_QRY to find the port 
    Returns:
        Serial object of arduino / teensy
    """
    # what my PC says the teensy LC is called, could use COM7 but that could change
    signal.signal(signal.SIGINT, signal.default_int_handler)
    serial_port = load_port(SERIAL_QRY, False) 

    if serial_port is None:
        raise Exception(f"Failed to load serial qry: {SERIAL_QRY}")
        
    arduino = serial.Serial(port=serial_port, baudrate=9600,  timeout=1.2)
    if arduino is None:
        raise Exception(f"Failed to mount Serial port: {SERIAL_QRY}")

    return arduino
# end init_arduino

def init_gui() -> MacroDisplay:
    """
    Initialize the gui, uses global root var. 
    Returns:
        MacroDisplay object for GUI
    """
    global root
    root = Tk()
    macro_display = MacroDisplay(root, "MODE")
    
    root.protocol("WM_DELETE_WINDOW", handle_close)
    root.iconbitmap(ICON_PATH)
    root.resizable(False, False)

    posX = None
    posY = None

    # Set window location + size
    if SECOND_MONITOR:
        posX = root.winfo_screenwidth() + int(root.winfo_screenwidth() / 2)
        posY = root.winfo_screenheight() - int(root.winfo_screenheight() / 2)
    else:
        posX = int(root.winfo_screenwidth() / 2)
        posY = int(root.winfo_screenheight() / 2)
    root.geometry(f"456x300+{posX}+{posY}")
    return macro_display
# end init_gui

def main_loop(arduino, root, macro_display):
    """
    Thread that handles serial comms and updates the GUI
    """
    while True:
        data = str(arduino.readline().decode())
        if data != "" and DEBUG:
            print(data)

        if data.startswith("key:"):
            keyPressed = int(data.split(":")[1].strip())
            print(f"Key pressed: {keyPressed}")

        if data.startswith("secmode:"):
            mode = int(data.split(":")[1].strip())
            macro_display.update_mode(switchMode(mode).name)

        if data.startswith("mode:"):
            mode = int(data.split(":")[1].strip())
            macro_display.update_mode(switchMode(mode).name, verbose=True)
            playsound(SFX_PATH, False)

        if data.startswith("log:"):
            print(data)
        
        # If X GUI btn was pressed, stop this thread
        if do_close:
            break
    # end loop
# end main_loop

def load_port(name: str, is_COM_name: bool = True) -> str:
    """
    Gets the COM port as a str that the teensy is connected to
    params:
        name - name of what you want to match (e.g. COM1)
        is_COM_name - is this a COM name or description? (e.g. COM1 vs USB Serial Device (COM1))
    Returns:
        Serial COM port as str
    """
    ports = list(serial.tools.list_ports.comports())
    if DEBUG:
        print("Serial Ports:")
    for p in ports:
        if DEBUG:
            print(f"{p.name} - {p.description}")
        if is_COM_name:
            if p.name == name:
                return p.name
        else:
            if name in p.description:
                return p.name
    return None
# end load_port


def handle_close():
    """
    Handles the close button operation, cleanup stuff
    """
    if thread1 is not None:
        do_close = True
        root.destroy()
        exit(0)
    else:
        print("thread is none")
        root.destroy()
        exit(0)
    # stop thread1
# end handle_close

if __name__ == "__main__":
    main()
