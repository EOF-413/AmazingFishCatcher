import os
import sys
import glob
import gc

import cv2

from config import KEYS, MIN_DEF_KEYS, MIN_DIG_KEYS


os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ['OPENCV_OPENCL_DEVICE'] = 'GPU'
os.environ['OPENCV_OPENCL_RUNTIME'] = 'nvidia'


class CUDAChecker:
    @staticmethod
    def check():
        try:
            import cv2
            cuda_count = cv2.cuda.getCudaEnabledDeviceCount()
            if cuda_count == 0:
                return {'available': False, 'message': 'CUDA устройства не найдены', 'devices': []}

            cv2.cuda.setDevice(0)
            devices = []
            for i in range(cuda_count):
                cv2.cuda.setDevice(i)
                devices.append({
                    'id': i,
                    'name': cv2.cuda.DeviceInfo(i).name(),
                    'memory': cv2.cuda.DeviceInfo(i).totalMemory(),
                })

            return {
                'available': True,
                'message': f'Найдено {cuda_count} CUDA устройств',
                'devices': devices,
                'current_device': devices[0] if devices else None
            }

        except Exception as e:
            return {'available': False, 'message': f'Ошибка CUDA: {str(e)}', 'devices': []}


CUDA_STATUS = CUDAChecker.check()
CUDA_AVAILABLE = CUDA_STATUS['available']


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Matcher:
    def __init__(self, folder="templates"):
        self.folder = folder
        self.use_gpu = CUDA_AVAILABLE
        self.templates = {}
        self.templates_gpu = {}
        self.gpu_info = CUDA_STATUS

        self.load_templates()

        print(f"[MATCHER] Режим: {'GPU (CUDA)' if self.use_gpu else 'CPU'}")
        if self.use_gpu:
            print(f"[MATCHER] Видеокарта: {self.gpu_info['current_device']['name']}")
        print(f"[MATCHER] Шаблонов загружено: {len(self.templates)}")

    def get_gpu_status(self):
        if self.use_gpu:
            device = self.gpu_info['current_device']
            return f"✅ GPU (CUDA) - {device['name']} ({device['memory'] // (1024**3)} GB)"
        else:
            return "❌ CPU (без CUDA)"

    def load_templates(self):
        self.templates.clear()
        self.templates_gpu.clear()

        path = resource_path(self.folder)
        keys = sorted(KEYS, key=len, reverse=True)

        for f in glob.glob(os.path.join(path, "*.png")):
            name = os.path.splitext(os.path.basename(f))[0].upper()
            matched = next((k for k in keys if name.startswith(k)), name)

            img = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue

            _, img = cv2.threshold(
                img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )

            self.templates.setdefault(matched, []).append(img)

            if self.use_gpu:
                try:
                    gpu_img = cv2.cuda_GpuMat()
                    gpu_img.upload(img)
                    self.templates_gpu.setdefault(matched, []).append(gpu_img)
                except Exception as e:
                    print(f"[GPU] Ошибка загрузки {name}: {e}")
                    self.use_gpu = False
                    break

    def reload(self):
        global CUDA_AVAILABLE, CUDA_STATUS

        CUDA_STATUS = CUDAChecker.check()
        CUDA_AVAILABLE = CUDA_STATUS['available']

        self.use_gpu = CUDA_AVAILABLE
        self.gpu_info = CUDA_STATUS
        self.load_templates()
        gc.collect()

        print(f"[MATCHER] Перезагружено, режим: {'GPU' if self.use_gpu else 'CPU'}")

    def process(self, gray):
        if self.use_gpu and self.templates_gpu:
            try:
                return self._process_gpu(gray)
            except Exception as e:
                print(f"[GPU] Ошибка, переключение на CPU: {e}")
                self.use_gpu = False
                return self._process_cpu(gray)
        return self._process_cpu(gray)

    def _process_gpu(self, gray):
        gpu_gray = cv2.cuda_GpuMat()
        gpu_gray.upload(gray)

        best_score = -1.0
        best_key = None

        for key, tlist in self.templates_gpu.items():
            for t in tlist:
                if gray.shape[0] < t.rows or gray.shape[1] < t.cols:
                    continue

                result = cv2.cuda.matchTemplate(
                    gpu_gray, t, cv2.TM_CCOEFF_NORMED
                )

                result_cpu = result.download()
                _, max_val, _, _ = cv2.minMaxLoc(result_cpu)

                if max_val > best_score:
                    best_score = max_val
                    best_key = key

                del result
                gc.collect()

        del gpu_gray
        gc.collect()

        return self._check_threshold(best_key, best_score)

    def _process_cpu(self, gray):
        best_score = -1.0
        best_key = None

        for key, tlist in self.templates.items():
            for t in tlist:
                if gray.shape[0] < t.shape[0] or gray.shape[1] < t.shape[1]:
                    continue

                result = cv2.matchTemplate(gray, t, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(result)

                if max_val > best_score:
                    best_score = max_val
                    best_key = key

        return self._check_threshold(best_key, best_score)

    def _check_threshold(self, key, score):
        if key is None:
            return None, 0.0

        threshold = (
            MIN_DEF_KEYS
            if key in ('L_ALT', 'L_SHIFT', 'L_CTRL')
            else MIN_DIG_KEYS
        )

        if score >= threshold:
            return key, round(score * 100, 2)

        return None, round(score * 100, 2)
