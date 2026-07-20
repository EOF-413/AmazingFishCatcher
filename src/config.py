import os
import json

VER = "1.0.1"
APP_NAME = "AFC"
APP_FULL_NAME = "Amazing Fish Catcher"

FISH_REGION = (945, 950, 35, 35)
KEY_REGION = (935, 875, 70, 20)

DIG = ['SHIFT', 'CTRL', 'SPACE']
DEF = ['D', 'S', 'W', 'V', 'C']

DEFAULT_CONFIG = {
    "HOLD": 0.1,
    "COOLDOWN": 0.01,
    "MIN_KEY_MATCH": 0.60,
    "MIN_ICON_MATCH": 0.70,
    "ALWAYS_ON_TOP": True,
    "AUTO_START": True,
    "MINIMIZE_TO_TRAY": False,
}


def get_config_path():
    app_data = os.getenv('APPDATA')
    config_dir = os.path.join(app_data, 'EOF-413', APP_NAME)
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    return os.path.join(config_dir, 'config.json')


def load_config():
    config_path = get_config_path()
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            for key, val in DEFAULT_CONFIG.items():
                if key not in config:
                    config[key] = val
            return config
    except (FileNotFoundError, json.JSONDecodeError):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()


def save_config(data):
    config_path = get_config_path()
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
