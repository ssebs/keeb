#!/usr/bin/env python3
# macrodisplay.py  - display what the macros actually are on a component
from tkinter import *
from tkinter import ttk
from util import MACRO_ITEMS


class MacroDisplay(ttk.Frame):
    """
    TK Frame class for the Macro Display
    """

    def __init__(self, container: Tk, mode: str, **options):
        """
        Constructor
        """
        super().__init__(container, **options)
        self.container = container
        self.mode = mode
        
        s = ttk.Style()
        s.configure('.', font=('Ubuntu-Mono', 16), relief='flat')

        self.grid(row=4, column=3)
        self.size = {"x": 3, "y": 4}

        # ttk.Label(container, text="Hello World!").grid(column=0, row=0)
        # ttk.Button(container, text="Quit", command=container.destroy).grid(column=1, row=0)

        grid = self._init_grid()
        self.lbl = ttk.Label(self.container, text=self.mode)
        self.lbl.grid(row=0, column=0, padx=5, pady=10)

    def update_mode(self, modeTxt: str):
        self.mode = modeTxt
        self.lbl.text = modeTxt

    def _init_grid(self) -> dict:
        grid = {}
        r = self.size["y"]
        c = 0
        for item in MACRO_ITEMS["VAL"]:

            print(f"{item['text']} - r: {r}, c: {c}")
            # plus 1 b/c we're starting on 1,1
            grid[item["pos"]] = ttk.Button(self.container, text=item["text"])
            grid[item["pos"]].grid(row=r, column=c, ipadx=0, ipady=15, padx=5, pady=10)
            grid[item["pos"]].state(["disabled"])

            # Increment
            if item["pos"] % 3 == 0:
                r -= 1
                c = 0
            else:
                c += 1
        return grid
