from time import sleep
from pynput.keyboard import Key, Controller
from src.config import DEF, DIG

keyboard = Controller()

dig = {
    'shift': Key.shift,
    'ctrl': Key.ctrl,
    'space': Key.space
}


def press_key(key, hold):
    key = key.lower()

    if key in dig:
        keyboard.press(dig[key])
        sleep(hold)
        keyboard.release(dig[key])
    else:
        keyboard.press(key)
        sleep(hold)
        keyboard.release(key)


def release_all():
    for key in DIG:
        if key.lower() in dig:
            keyboard.release(dig[key.lower()])

    for key in DEF:
        try:
            keyboard.release(key.lower())
        except ValueError:
            pass
