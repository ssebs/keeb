#!/usr/bin/env python3
# notify.py - Notify user of keyboard mode switches

import time
import signal
import sys

import serial
import serial.tools.list_ports
from win10toast import ToastNotifier

from util import switchMode

DEBUG = False

def main():
    print("Client for macro pad")
    signal.signal(signal.SIGINT, signal.default_int_handler)
    serial_port = load_port("COM6")
    arduino = serial.Serial(port=serial_port, baudrate=2000000,  timeout=.5)
    toast = ToastNotifier()

    if arduino is None:
        print("Failed to mount COM6")

    while True:
        data = str(arduino.readline().decode())
        if data != "" and DEBUG: 
            print(data)
        if data.startswith("mode:"):
            mode = int(data.split(":")[1].strip())
            print(switchMode(mode).name)
            toast.show_toast("Keyboard mode:", switchMode(mode).name, duration=2, icon_path='')


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
