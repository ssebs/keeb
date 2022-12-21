# keeb

keyboard firmware for my macropad

Will add screenshots and wiring diagram stuff later.

basically, it's 9 keys 3 rows 3 cols and a separate switch on pin8

## client
A python script that will notify when the keeb mode switches

## Install dependencies
- python3
- `cd client/`
    - `python3 -m venv venv`
    - `.\venv\Scripts\Activate.ps1`
    - `pip install -r requirements.txt`

### Building the .exe
- `pyinstaller -c -F client/notify.py`
    - Built file is under `./dist/`

