#!/usr/bin/env python3
# macrodisplay.py  - display what the macros actually are on a component
from tkinter import *
from tkinter import ttk
from util import MACRO_ITEMS


class MacroDisplay(ttk.Frame):
    """
    TK Frame class for the Macro Display
    Params:
        container - Tk root container
        mode - str mode to cross reference against MACRO_ITEMS
        **options - other options to be passed to tk
    Methods:
        update_mode - update the mode and rebuild grid with new data. Cross references MACRO_ITEMS
    """

    def __init__(self, container: Tk, mode: str, **options):
        """
        Constructor
        """
        super().__init__(container, **options)
        self.container = container
        self.mode = StringVar(value=mode)
        self.status = StringVar(value="Status...")

        s = ttk.Style()
        s.configure('.', font=('Ubuntu-Mono', 16), relief='flat')

        self.grid(row=4, column=3)
        self.size = {"x": 3, "y": 4}

        self.macrogrid = self._init_grid()
        self.lbl = ttk.Label(self.container, textvariable=self.mode)
        self.lbl.grid(row=0, column=0, padx=5, pady=10)

        self.status_lbl = ttk.Label(self.container, textvariable=self.status)
        self.status_lbl.grid(row=0, column=1, columnspan=2, padx=5, pady=10)
    # end __init__

    def update_mode(self, modeTxt: str, verbose: bool = False):
        """
        Updates the mode and reloads the grid depending on the modeTxt. Cross references MACRO_ITEMS
        Params:
            modeTxt - str the name of the mode (e.g. NUMPAD, VAL, HELPER)
            verbose - bool [False] add verbosity
        """
        self.mode.set(modeTxt)
        self.macrogrid = None
        self.macrogrid = self._init_grid()
        if verbose:
            print(f"Updating mode! {modeTxt}")
    # end update_mode

    def update_status(self, statusTxt: str, position: int, verbose: bool = False):
        """
        Updates the status text
        Params:
            statusTxt - str the name of the mode (e.g. NUMPAD, VAL, HELPER)
            position - int valstrings position
            verbose - bool [False] add verbosity
        """
        if self.status.get() != statusTxt:
            self.status.set(statusTxt)
            if verbose:
                print(f"Updating status! {statusTxt}")
        else:
            if verbose:
                print("No change needed to status")

    # end update_status

    def _init_grid(self, verbose: bool = False) -> dict:
        # TODO add option for val strings
        """
        Initializes the grid using self.mode's value cross referenced with MACRO_ITEMS' items
        Params:
            verbose - bool [False] add verbosity
        Returns:
            dict of ttk grid buttons
        """
        grid = {}
        r = self.size["y"]
        c = 0
        for item in MACRO_ITEMS[self.mode.get()]:
            if verbose:
                print(f"{item['text']} - r: {r}, c: {c}")
            # plus 1 b/c we're starting on 1,1
            grid[item["pos"]] = ttk.Button(self.container, text=item["text"])
            grid[item["pos"]].grid(
                row=r, column=c, ipadx=0, ipady=15, padx=5, pady=10)
            grid[item["pos"]].state(["disabled"])

            # Increment
            if item["pos"] % 3 == 0:
                r -= 1
                c = 0
            else:
                c += 1
        return grid
    # end _init_grid
