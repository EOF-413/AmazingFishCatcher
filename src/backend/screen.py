import ctypes

from src.config import FISH_REGION, KEY_REGION


def get_key_region():
    user32 = ctypes.windll.user32
    w = user32.GetSystemMetrics(0)
    h = user32.GetSystemMetrics(1)

    x, y, width, height = KEY_REGION

    scale_x = w / 1920
    scale_y = h / 1080

    left = int(x * scale_x)
    top = int(y * scale_y)
    right = int((x + width) * scale_x)
    bottom = int((y + height) * scale_y)

    return (left, top, right, bottom)


def get_fish_region():
    user32 = ctypes.windll.user32
    w = user32.GetSystemMetrics(0)
    h = user32.GetSystemMetrics(1)

    x, y, width, height = FISH_REGION

    scale_x = w / 1920
    scale_y = h / 1080

    left = int(x * scale_x)
    top = int(y * scale_y)
    right = int((x + width) * scale_x)
    bottom = int((y + height) * scale_y)

    return (left, top, right, bottom)
