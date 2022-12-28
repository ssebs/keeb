#!/usr/bin/env python3
# macrodisplay.py  - display what the macros actually are on a component
from tkinter import *
from tkinter import ttk
from util import MACRO_ITEMS

class MacroDisplay(ttk.Frame):
    """
    TK Frame class for the Macro Display
    """
    def __init__(self, container: Tk, **options):
        """
        Constructor
        """
        super().__init__(container, **options)
        self.container = container
        self.grid(row=3, column=4)
        ttk.Label(container, text="Hello World!").grid(column=0, row=0)
        ttk.Button(container, text="Quit", command=container.destroy).grid(column=1, row=0)

        grid = self._init_grid()

    def _init_grid(self) -> dict:
        grid = {}
        r = 0
        c = 0
        for item in MACRO_ITEMS["VAL"]:
            
            print(f"{item['text']} - r: {r}, c: {c}")
            # plus 1 b/c we're starting on 1,1
            grid[item["pos"]] = ttk.Label(self.container, text=item["text"]).grid(row=r+1, column=c)

            # Increment
            if item["pos"] % 3 == 0:
                r += 1
                c = 0
            else:
                c += 1
        return grid

