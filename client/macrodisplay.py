#!/usr/bin/env python3
# macrodisplay.py  - display what the macros actually are on a component
from tkinter import StringVar, Tk
from tkinter import ttk
from util import MACRO_ITEMS, VAL_STRINGS, MyLabel


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
    STATUS_DEFAULT_TXT = "Status..."
    LAST_QUOTE_DEFAULT_TXT = "Last Quote <="
    NEXT_QUOTE_DEFAULT_TXT = "Next Quote =>"

    def __init__(self, container: Tk, mode: str, **options):
        """
        Constructor
        """
        super().__init__(container, **options)
        self.truncate_length = 28
        self.container = container
        self.mode = StringVar(value=mode)
        self.status = StringVar(value=MacroDisplay.STATUS_DEFAULT_TXT)
        self.next_txt = StringVar(value=MacroDisplay.NEXT_QUOTE_DEFAULT_TXT)
        self.last_txt = StringVar(value=MacroDisplay.LAST_QUOTE_DEFAULT_TXT)

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
        if self.mode.get() != modeTxt:
            self.mode.set(modeTxt)
            self.macrogrid = None
            self.macrogrid = self._init_grid()
            if verbose:
                print(f"Updating mode! {modeTxt}")
    # end update_mode

    def update_status(self, position: int, verbose: bool = False):
        """
        Updates the status text
        Params:
            position - int valstrings position
            verbose - bool [False] add verbosity
        """
        # Check for dupe status (VAL, HELPER, etc)
        if position >= len(VAL_STRINGS):
            if verbose:
                print(f"POS too big")
            position -= 1
        if self.status.get() not in VAL_STRINGS[position]:

            # Trim the string
            if len(VAL_STRINGS[position]) >= self.truncate_length:
                self.status.set(VAL_STRINGS[position][:self.truncate_length])
            else:
                self.status.set(VAL_STRINGS[position])

            # Get correct position of last and next item
            next_pos = position + 1 if position < len(VAL_STRINGS) - 1  else 0
            last_pos = position - 1 if position > 0 else -1
            if verbose:
                print(f"Pos: {position}")
                print(f"Next Pos: {next_pos}")
                print(f"Last Pos: {last_pos}")

            # Update textboxes if not already set
            if self.next_txt.get() not in VAL_STRINGS[next_pos]:
                self.next_txt.set(VAL_STRINGS[next_pos])
      
            if self.last_txt.get() not in VAL_STRINGS[last_pos]:
                self.last_txt.set(VAL_STRINGS[last_pos])
      
            if verbose:
                print(f"Updating status - {VAL_STRINGS[position]}")
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
        # TODO: use self.grid instead...
        grid = {}
        r = self.size["y"]
        c = 0
        for item in MACRO_ITEMS[self.mode.get()]:
            if verbose:
                print(f"{item['text']} - r: {r}, c: {c}")

            # plus 1 b/c we're starting on 1,1
            # If in certain col, make variable text, otherwise grab default
            if item["text"] == self.next_txt.get() or item["text"] == MacroDisplay.NEXT_QUOTE_DEFAULT_TXT:
                # grid[item["pos"]] = MyLabel(self.container, textvariable=self.next_txt, width=12, borderwidth=2, color='red')
                grid[item["pos"]] = ttk.Label(self.container, textvariable=self.next_txt, width=12)
            elif item["text"] == self.last_txt.get() or item["text"] == MacroDisplay.LAST_QUOTE_DEFAULT_TXT:
                grid[item["pos"]] = ttk.Label(self.container, textvariable=self.last_txt, width=12)
            else:
                grid[item["pos"]] = ttk.Label(self.container, text=item["text"], width=12)
            
            grid[item["pos"]].grid(
                row=r, column=c, ipadx=0, ipady=15, padx=5, pady=10)

            # Increment
            if item["pos"] % 3 == 0:
                r -= 1
                c = 0
            else:
                c += 1
        return grid
    # end _init_grid
