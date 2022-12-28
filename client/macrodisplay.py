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
        self.mode = StringVar(value=mode)
        
        s = ttk.Style()
        s.configure('.', font=('Ubuntu-Mono', 16), relief='flat')

        self.grid(row=4, column=3)
        self.size = {"x": 3, "y": 4}

        self.macrogrid = self._init_grid()
        self.lbl = ttk.Label(self.container, textvariable=self.mode)
        self.lbl.grid(row=0, column=0, padx=5, pady=10)

    def update_mode(self, modeTxt: str, is_auto: bool = False, verbose: bool = False):
        self.mode.set(modeTxt)
        self.macrogrid = None
        self.macrogrid = self._init_grid()
        if verbose:
            print(f"Updating mode! {modeTxt}")

    def _init_grid(self, verbose: bool = False) -> dict:
        grid = {}
        r = self.size["y"]
        c = 0
        for item in MACRO_ITEMS[self.mode.get()]:
            if verbose:
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
