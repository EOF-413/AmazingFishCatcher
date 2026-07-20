import cv2
from pathlib import Path

from src.config import load_config


class KeyMatcher:
    def __init__(self):
        config = load_config()
        self.threshold = config.get("MIN_KEY_MATCH", 0.40)
        self.keys_folder = Path("Keys")
        self.keys_cache = {}
        self.templates = {}
        self._load_keys()

    def _load_keys(self):
        if not self.keys_folder.exists():
            return

        for file_path in self.keys_folder.glob("*.png"):
            key_name = file_path.stem
            image = cv2.imread(str(file_path), cv2.IMREAD_GRAYSCALE)
            if image is not None:
                self.keys_cache[key_name] = image
                self.templates[key_name] = image

    def update_threshold(self, threshold):
        self.threshold = threshold

    def match(self, screen_image, key_name=None):
        if screen_image is None:
            return None, 0.0

        if len(screen_image.shape) == 3:
            screen_gray = cv2.cvtColor(screen_image, cv2.COLOR_BGR2GRAY)
        else:
            screen_gray = screen_image

        if key_name and key_name in self.keys_cache:
            template = self.keys_cache[key_name]
            is_match, percentage = self._compare_images(screen_gray, template)
            if is_match:
                return key_name, percentage
            return None, percentage

        best_match = None
        best_percentage = 0.0

        for name, template in self.keys_cache.items():
            is_match, percentage = self._compare_images(screen_gray, template)
            if percentage > best_percentage:
                best_percentage = percentage
                if is_match:
                    best_match = name

        return best_match, best_percentage

    def _compare_images(self, screen_image, template):
        if screen_image is None or template is None:
            return False, 0.0

        try:
            if (screen_image.shape[0] >= template.shape[0] and
                    screen_image.shape[1] >= template.shape[1]):
                result = cv2.matchTemplate(
                    screen_image, template, cv2.TM_CCOEFF_NORMED
                )
                _, max_val, _, _ = cv2.minMaxLoc(result)
            else:
                template_resized = cv2.resize(
                    template, (screen_image.shape[1], screen_image.shape[0])
                )
                result = cv2.matchTemplate(
                    screen_image, template_resized, cv2.TM_CCOEFF_NORMED
                )
                _, max_val, _, _ = cv2.minMaxLoc(result)

            is_match = max_val >= self.threshold
            return is_match, max_val
        except cv2.error:
            return False, 0.0


class FishMatcher:
    def __init__(self):
        config = load_config()
        self.threshold = config.get("MIN_ICON_MATCH", 0.70)
        self.fishs_folder = Path("Fishs")
        self.fishs_cache = {}
        self.templates = {}
        self._load_fishs()

    def _load_fishs(self):
        if not self.fishs_folder.exists():
            return

        for file_path in self.fishs_folder.glob("*.png"):
            fish_name = file_path.stem
            image = cv2.imread(str(file_path), cv2.IMREAD_GRAYSCALE)
            if image is not None:
                self.fishs_cache[fish_name] = image
                self.templates[fish_name] = image

    def update_threshold(self, threshold):
        self.threshold = threshold

    def match(self, area_image, fish_name=None):
        if area_image is None:
            return None, 0.0

        if len(area_image.shape) == 3:
            area_gray = cv2.cvtColor(area_image, cv2.COLOR_BGR2GRAY)
        else:
            area_gray = area_image

        if fish_name and fish_name in self.fishs_cache:
            template = self.fishs_cache[fish_name]
            is_match, percentage = self._compare_images_with_scaling(
                area_gray, template
            )
            if is_match:
                return fish_name, percentage
            return None, percentage

        best_match = None
        best_percentage = 0.0

        for name, template in self.fishs_cache.items():
            is_match, percentage = self._compare_images_with_scaling(
                area_gray, template
            )
            if percentage > best_percentage:
                best_percentage = percentage
                if is_match:
                    best_match = name

        return best_match, best_percentage

    def _compare_images_with_scaling(self, area_image, template):
        if area_image is None or template is None:
            return False, 0.0

        try:
            best_score = 0.0

            h_area, w_area = area_image.shape
            h_template, w_template = template.shape

            scales = [0.3, 0.4, 0.5, 0.6]

            for scale in scales:
                new_w = int(w_template * scale)
                new_h = int(h_template * scale)

                if new_w < 10 or new_h < 10:
                    continue

                if new_w > w_area or new_h > h_area:
                    continue

                template_scaled = cv2.resize(template, (new_w, new_h))
                result = cv2.matchTemplate(
                    area_image, template_scaled, cv2.TM_CCOEFF_NORMED
                )
                _, max_val, _, _ = cv2.minMaxLoc(result)

                if max_val > best_score:
                    best_score = max_val

                    if best_score >= self.threshold:
                        return True, best_score

            is_match = best_score >= self.threshold
            return is_match, best_score
        except cv2.error:
            return False, 0.0

    def _compare_images(self, area_image, template):
        if area_image is None or template is None:
            return False, 0.0

        try:
            if (area_image.shape[0] >= template.shape[0] and
                    area_image.shape[1] >= template.shape[1]):
                result = cv2.matchTemplate(
                    area_image, template, cv2.TM_CCOEFF_NORMED
                )
                _, max_val, _, _ = cv2.minMaxLoc(result)
            else:
                template_resized = cv2.resize(
                    template, (area_image.shape[1], area_image.shape[0])
                )
                result = cv2.matchTemplate(
                    area_image, template_resized, cv2.TM_CCOEFF_NORMED
                )
                _, max_val, _, _ = cv2.minMaxLoc(result)

            is_match = max_val >= self.threshold
            return is_match, max_val
        except cv2.error:
            return False, 0.0
