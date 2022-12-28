# keeb

Keyboard firmware and driver for my macropad. Using a Teensy LC.

## Firmware / arduino stuff
See `keeb/keeb.ino` for more details, but basically theres a few modes, and a mode switcher, and 9 buttons. Button/pin mappings are done in that file.

### Grid
Here's what the grid looks like physically:
```
[ ] [ ] [ ]
[ ] [ ] [ ]
[ ] [ ] [ ]
    [ ]
```

Here's what the buttons map to:
```
[7] [8] [9]
[4] [5] [6]
[1] [2] [3]
    [m]
```
`1 - 9` are like numpad btns, see `MACRO_ITEMS` for what they do.
`m` is the mode switcher.

> Will add screenshots and wiring diagram stuff later. Basically, it's 9 keys 3 rows 3 cols and a separate switch on pin8

## client
A python GUI that shows what mode you're in and what the buttons do. Data is sourced from util.py's MACRO_ITEMS

## Install dependencies
- python3
- `cd client/`
    - `python3 -m venv venv`
    - `.\venv\Scripts\Activate.ps1`
    - `pip install -r requirements.txt`

### Building the .exe
- `pyinstaller -c -F client/notify.py`
    - Built file is under `./dist/`

