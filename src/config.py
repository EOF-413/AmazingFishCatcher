import os
import json

VER = "3.1.0"
APP_NAME = "ASC"
APP_FULL_NAME = "Amazing Street Cleaner"

X1_RATIO = 0.4427
Y1_RATIO = 0.6944
X2_RATIO = 0.5547
Y2_RATIO = 0.8102

KEYS = ['SHIFT', 'CTRL', 'ALT', 'A', 'C', 'D', 'E', 'J', 'K', 'L', 'N', 'Q', 'R', 'S', 'W']

DEFAULT_CONFIG = {
    "HOLD": 1.25,
    "COOLDOWN": 0.75,
    "MIN_MATCH": 0.40,
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
