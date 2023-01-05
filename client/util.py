#!/usr/bin/env python3
# util.py - Util stuff
from enum import Enum
from tkinter import ttk


class switchMode (Enum):
    NUMPAD = 0
    VAL = 1
    HELPER = 2
    _NUM_MODES = 3


MACRO_ITEMS = {
    "NUMPAD": [
        {
            "pos": 1,
            "text": "1"
        },
        {
            "pos": 2,
            "text": "2"
        },
        {
            "pos": 3,
            "text": "3"
        },
        {
            "pos": 4,
            "text": "4"
        },
        {
            "pos": 5,
            "text": "5"
        },
        {
            "pos": 6,
            "text": "6"
        },
        {
            "pos": 7,
            "text": "7"
        },
        {
            "pos": 8,
            "text": "8"
        },
        {
            "pos": 9,
            "text": "9"
        },
    ],
    "VAL": [
        {
            "pos": 1,
            "text": "Last Quote <="
        },
        {
            "pos": 2,
            "text": "Pickup Line ;)"
        },
        {
            "pos": 3,
            "text": "Next Quote =>"
        },
        {
            "pos": 4,
            "text": "gg"
        },
        {
            "pos": 5,
            "text": "ggwp"
        },
        {
            "pos": 6,
            "text": "ggez"
        },
        {
            "pos": 7,
            "text": "nt"
        },
        {
            "pos": 8,
            "text": "nice"
        },
        {
            "pos": 9,
            "text": "Nice!"
        },
    ],
    "HELPER": [
        {
            "pos": 1,
            "text": "gg"
        },
        {
            "pos": 2,
            "text": "val pickup line"
        },
        {
            "pos": 3,
            "text": "incognito"
        },
        {
            "pos": 4,
            "text": "undo"
        },
        {
            "pos": 5,
            "text": "gta heal"
        },
        {
            "pos": 6,
            "text": ""
        },
        {
            "pos": 7,
            "text": "Grass Canada"
        },
        {
            "pos": 8,
            "text": "Grass Yoda"
        },
        {
            "pos": 9,
            "text": "Grass Allergic"
        },
    ],
    "MODE": [
        {
            "pos": 1,
            "text": "1"
        },
        {
            "pos": 2,
            "text": "2"
        },
        {
            "pos": 3,
            "text": "3"
        },
        {
            "pos": 4,
            "text": "4"
        },
        {
            "pos": 5,
            "text": "5"
        },
        {
            "pos": 6,
            "text": "6"
        },
        {
            "pos": 7,
            "text": "7"
        },
        {
            "pos": 8,
            "text": "8"
        },
        {
            "pos": 9,
            "text": "9"
        },
    ]
}

VAL_STRINGS = [
    "Sheeeeeeeeeeeeeeeeeeeeeeeeesh",
    "You were a boulder. I am a mountain!",
    "How did every piece of trash end up on the same team?",
    "Just some good old hard yakka, standing in between us and victory.",
    "Oi! I'm pissed!",
    "Bloinded",
    "I am on a higher plane, chale, literally!",
    "Activating kill mode. That's a joke. Kill mode is default.",
    "Buy stuff, kaching, lil' skkkrrrr, then we're done, yeah?",
    "Yo!    Nice.",
    "Sheee-achoo!-eeesh!",
]

class MyLabel(ttk.Frame):
    '''inherit from Frame to make a label with customized border'''
    def __init__(self, parent, myborderwidth=0, color=None,
                 myborderplace='center', *args, **kwargs):
        s = ttk.Style()
        s.configure('TFrame', background=color)
        self.frame = ttk.Frame.__init__(self, parent)
        self.propagate(False) # prevent frame from auto-fitting to contents
        self.label = ttk.Label(self.frame, *args, **kwargs) # make the label

        # pack label inside frame according to which side the border
        # should be on. If it's not 'left' or 'right', center the label
        # and multiply the border width by 2 to compensate
        if myborderplace == 'left':
            self.label.pack(side=RIGHT)
        elif myborderplace == 'right':
            self.label.pack(side=LEFT)
        else:
            self.label.pack()
            myborderwidth = myborderwidth * 2

        # set width and height of frame according to the req width
        # and height of the label
        self.config(width=self.label.winfo_reqwidth() + myborderwidth)
        self.config(height=self.label.winfo_reqheight())