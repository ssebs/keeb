#!/usr/bin/env python3
# util.py - Util stuff
from enum import Enum


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
            "text": "last quote"
        },
        {
            "pos": 2,
            "text": "random quote"
        },
        {
            "pos": 3,
            "text": "next quote"
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
            "text": "ntnt"
        },
        {
            "pos": 9,
            "text": "?"
        },
    ],
    "HELPER": [
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
