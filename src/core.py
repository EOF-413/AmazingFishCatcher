from time import sleep
from threading import Thread

import cv2
import numpy as np
from PIL import ImageGrab
from pynput.keyboard import Listener, Key, Controller

from src.backend import KeyMatcher, FishMatcher
from src.backend import get_fish_region, get_key_region, press_key, release_all
from src.config import load_config


class App:
    def __init__(self):
        self.key_matcher = KeyMatcher()
        self.fish_matcher = FishMatcher()
        self.fish_region = get_fish_region()
        self.key_region = get_key_region()
        self.enabled = False
        self.running = True
        self.loop_thread = None
        self.gui = None
        self.listener = None
        self.last_press_time = 0
        self.keyboard = Controller()

    def loop(self):
        while self.running:
            if not self.enabled:
                sleep(0.05)
                continue

            try:
                config = load_config()

                self.fish_matcher.update_threshold(config["MIN_ICON_MATCH"])
                self.key_matcher.update_threshold(config["MIN_KEY_MATCH"])

                fish_screenshot = ImageGrab.grab(bbox=self.fish_region)
                fish_image_rgb = np.array(fish_screenshot)
                fish_image_bgr = cv2.cvtColor(fish_image_rgb, cv2.COLOR_RGB2BGR)

                key_screenshot = ImageGrab.grab(bbox=self.key_region)
                key_gray = np.array(key_screenshot.convert('L'), dtype=np.uint8)

                fish_name, fish_score = self.fish_matcher.match(fish_image_bgr)
                key_name, key_score = self.key_matcher.match(key_gray)

                if fish_name and key_name:
                    if self.gui:
                        self.gui.log(
                            f"Нажата клавиша {key_name} (Р: {fish_score*100:.1f}%, К: {key_score*100:.1f}%)",
                            'keyboard'
                        )

                    release_all()
                    sleep(0.02)

                    press_key(key_name, 0.1)

                    sleep(0.01)
                    release_all()

                elif fish_name and not key_name:
                    if self.gui:
                        self.gui.log(
                            f"Рыбка найдена, клавиша не определена (Р: {fish_score*100:.1f}%)",
                            'warning'
                        )

                elif not fish_name and key_name:
                    if self.gui:
                        self.gui.log(
                            f"Клавиша {key_name} найдена, рыбки нет (К: {key_score*100:.1f}%)",
                            'warning'
                        )

                else:
                    if self.gui:
                        self.gui.log(
                            f"Ничего не найдено (Р: {fish_score*100:.1f}%, К: {key_score*100:.1f}%)",
                            'nokey'
                        )

                sleep(config["COOLDOWN"])

            except Exception as e:
                if self.gui:
                    self.gui.log_error(f"Ошибка: {e}")
                sleep(0.5)

    def on_press(self, key):
        try:
            if key == Key.f9:
                if self.gui:
                    self.gui._on_toggle()
        except Exception:
            pass

    def start_listener(self):
        if self.listener is None or not self.listener.running:
            self.listener = Listener(on_press=self.on_press)
            self.listener.daemon = True
            self.listener.start()

    def start(self):
        if not self.enabled:
            self.enabled = True
            if self.gui:
                self.gui.log_info("Запущено")
                self.gui.update_status()
            if not self.loop_thread or not self.loop_thread.is_alive():
                self.loop_thread = Thread(target=self.loop, daemon=True)
                self.loop_thread.start()

    def stop(self):
        self.enabled = False
        release_all()
        if self.gui:
            self.gui.log_info("Остановлено")
            self.gui.update_status()

    def toggle(self):
        if self.enabled:
            self.stop()
        else:
            self.start()

    def cleanup(self):
        self.running = False
        self.enabled = False
        release_all()
        if self.listener and self.listener.running:
            self.listener.stop()
