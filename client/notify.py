#!/usr/bin/env python3
# notify.py - Notify user of keyboard mode switches

import time
import signal
import sys
import os
import threading

import serial
import serial.tools.list_ports
from playsound import playsound

from util import (
    switchMode, MACRO_ITEMS, VAL_STRINGS, SerialNotFoundException, SerialMountException, CustomSerialException
)
from macrodisplay import MacroDisplay
from tkinter import Tk, ttk, messagebox

RETRY_COUNT = 5
DEBUG = False
SECOND_MONITOR = False
ICON_PATH = 'bell.ico'
SFX_PATH = 'snap.mp3'
SERIAL_QRY = "USB Serial Device"
MSGBOX_TITLE = "Keeb - Serial Exception"


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
        os.path.abspath(__file__)) + "\\res")
    return os.path.join(base_path, relative_path)


def main():
    """
    Main function
    TODO: Make this OOP instead of using global vars and constants
    """
    if DEBUG:
        print("Client for macro pad")


    global arduino 
    global macro_display 

    arduino, macro_display = init()
    
    # Setup Serial comm thread
    global thread1
    # For the close icon in the GUI, stop the thread too
    global do_close
    do_close = False
    
    thread1 = threading.Thread(target=main_loop, args=(
        arduino, root, macro_display), daemon=True)
    thread1.start()

    # Start GUI thread (main)
    root.mainloop()
    if do_restart:
        print("Doing restart")
        print(thread1.is_alive())
        # main()
        arduino = init_arduino()
# end main

def init() -> tuple:
    # TODO: Cleanup
    for tries in range(RETRY_COUNT):
        try:
            arduino = init_arduino()
            macro_display = init_gui()  # sets global root, returns MacroDisplay
        except serial.SerialException as e:
            print(e)
            messagebox.showerror(title=MSGBOX_TITLE,
                                message=f"{str(e)}\n\nCheck if you have another instance open?")
            exit(0)
        except CustomSerialException as e:
            print(e)
            do_try_again = messagebox.askyesno(title=MSGBOX_TITLE,
                                message=f"{str(e)}\n\nWant to try loading again?")
            if do_try_again:
                continue
            else:
                exit(0)
        except Exception as e:
            print(e)
            raise e
            sys.exit(1)
        # break if trying succeeds
        break
    return (arduino, macro_display)


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
        raise SerialNotFoundException(
            f"Failed to load serial port: {SERIAL_QRY}")

    arduino = serial.Serial(port=serial_port, baudrate=9600,  timeout=1.2)
    if arduino is None:
        raise SerialMountException(
            f"Failed to mount Serial port: {SERIAL_QRY}")

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
    s = ttk.Style()
    s.configure('.', font=('Ubuntu-Mono', 16), relief='flat',
                foreground='#cccccc', background='#252525')
    s.configure('TFrame', foreground='#ffffff', background='#222222')

    main_frame = ttk.Frame(root)
    main_frame.pack()

    macro_display = MacroDisplay(main_frame, "MODE")

    root.protocol("WM_DELETE_WINDOW", handle_close)
    root.iconbitmap(resource_path(ICON_PATH))
    root.resizable(False, False)
    root.title("Keeb")

    posX = None
    posY = None

    # Set window location + size
    if SECOND_MONITOR:
        posX = root.winfo_screenwidth() + int(root.winfo_screenwidth() / 2)
        posY = root.winfo_screenheight() - int(root.winfo_screenheight() / 2)
    else:
        posX = int(root.winfo_screenwidth() / 2)
        posY = int(root.winfo_screenheight() / 2)
    root.geometry(f"475x280+{posX}+{posY}")
    return macro_display
# end init_gui


def main_loop(arduino, root, macro_display):
    """
    Thread that handles serial comms and updates the GUI
    """
    # To restart the program
    global do_restart
    do_restart = False
    while True:
        try:
            data = str(arduino.readline().decode())
        except serial.SerialException as e:
            print(e)
            do_restart = True
            break;
            
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
            macro_display.update_mode(switchMode(mode).name, verbose=False)
            playsound(resource_path(SFX_PATH), block=False)

        if data.startswith("valstr:"):
            pos = int(data.split(":")[1].strip())
            macro_display.update_status(pos)

        if data.startswith("log:"):
            print(data)

        # If X GUI btn was pressed, stop this thread
        if do_close:
            break
    # end loop
    if do_restart:
        root.destroy()
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
        sys.exit(0)
    else:
        print("thread is none")
        root.destroy()
        sys.exit(0)
    # stop thread1
# end handle_close


if __name__ == "__main__":
    main()
