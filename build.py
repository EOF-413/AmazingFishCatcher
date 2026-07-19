import os
import sys
import subprocess
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_NAME = 'ASC'

print("=" * 50)
print("AmazingStreetCleaner - Сборка .exe")
print("=" * 50)

for folder in ['dist', 'build']:
    folder_path = os.path.join(BASE_DIR, folder)
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"[CLEAN] Удалена папка {folder_path}")

cmd = [
    sys.executable, '-m', 'PyInstaller',
    '--noconsole',
    '--onedir',
    '--noupx',
    '--strip',
    '--exclude-module', 'matplotlib',
    '--exclude-module', 'scipy',
    '--exclude-module', 'numpy',
    '--exclude-module', 'PIL',
    '--exclude-module', 'cv2',
    '--exclude-module', 'PyQt5',
    '--exclude-module', 'pynput',
    '--exclude-module', 'setuptools',
    '--exclude-module', 'pip',
    '--exclude-module', 'pkg_resources',
    f'--name={APP_NAME}',
    'main.py'
]

icon_path = os.path.join(BASE_DIR, 'icon.ico')
if os.path.exists(icon_path):
    cmd.insert(4, f'--icon={icon_path}')
    print("[OK] Иконка найдена")

subprocess.run(cmd, cwd=BASE_DIR)

src_templates = os.path.join(BASE_DIR, 'templates')
dst_templates = os.path.join(BASE_DIR, 'dist', APP_NAME, 'templates')
if os.path.exists(src_templates):
    if os.path.exists(dst_templates):
        shutil.rmtree(dst_templates)
    shutil.copytree(src_templates, dst_templates)
    print("[OK] Папка templates скопирована")

dist_dir = os.path.join(BASE_DIR, 'dist', APP_NAME)
exe_path = os.path.join(BASE_DIR, 'dist', f'{APP_NAME}.exe')

if os.path.exists(exe_path):
    size = os.path.getsize(exe_path) / (1024 * 1024)
    print(f"\n✅ Сборка завершена! Размер: {size:.2f} MB")
else:
    print("\n❌ Ошибка сборки")

input("\nНажмите Enter для выхода...")
