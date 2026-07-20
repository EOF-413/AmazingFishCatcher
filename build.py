import os
import sys
import shutil
import subprocess
from src.config import VER, APP_NAME, APP_FULL_NAME

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print("=" * 60)
print(f"{APP_FULL_NAME} v{VER} - Сборка для установщика")
print("=" * 60)

for folder in ['dist', 'build']:
    folder_path = os.path.join(BASE_DIR, folder)
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

cmd = [
    sys.executable, '-m', 'PyInstaller',
    '--onedir',
    '--noconsole',
    '--strip',
    '--noupx',
    '--exclude-module', 'matplotlib',
    '--exclude-module', 'scipy',
    '--exclude-module', 'setuptools',
    '--exclude-module', 'pip',
    '--exclude-module', 'pkg_resources',
    '--exclude-module', 'PyInstaller',
    '--collect-all', 'pynput',
    '--collect-all', 'PIL',
    '--collect-all', 'numpy',
    '--collect-all', 'cv2',
    '--collect-all', 'PyQt5',
    '--paths', BASE_DIR,
    '--paths', os.path.join(BASE_DIR, 'src'),
    f'--name={APP_NAME}',
    'main.py'
]

icon_path = os.path.join(BASE_DIR, 'icon.ico')
if os.path.exists(icon_path):
    cmd.insert(4, f'--icon={icon_path}')

try:
    subprocess.run(cmd, cwd=BASE_DIR, check=True)
except subprocess.CalledProcessError as e:
    print(f"[ERROR] Ошибка сборки: {e}")
    sys.exit(1)

INSTALL_DIR = os.path.join(BASE_DIR, 'files')
if os.path.exists(INSTALL_DIR):
    shutil.rmtree(INSTALL_DIR)
os.makedirs(INSTALL_DIR)

APP_DIR = os.path.join(INSTALL_DIR, APP_NAME)
os.makedirs(APP_DIR)

dist_path = os.path.join(BASE_DIR, 'dist', APP_NAME)
if os.path.exists(dist_path):
    for item in os.listdir(dist_path):
        src = os.path.join(dist_path, item)
        dst = os.path.join(APP_DIR, item)
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

src_templates = os.path.join(BASE_DIR, 'templates')
dst_templates = os.path.join(APP_DIR, 'templates')
if os.path.exists(src_templates):
    shutil.copytree(src_templates, dst_templates)

src_icon = os.path.join(BASE_DIR, 'icon.ico')
if os.path.exists(src_icon):
    shutil.copy2(src_icon, APP_DIR)

run_script = f'''@echo off
title {APP_FULL_NAME} v{VER}
echo Starting {APP_FULL_NAME}...
echo.
"{APP_NAME}.exe"
echo.
echo Program finished. Press any key to exit...
pause > nul
'''

run_path = os.path.join(APP_DIR, 'run.bat')
with open(run_path, 'w', encoding='cp866') as f:
    f.write(run_script)

print(f"\nСодержимое {APP_DIR}:")
for item in os.listdir(APP_DIR):
    if os.path.isfile(os.path.join(APP_DIR, item)):
        size = os.path.getsize(os.path.join(APP_DIR, item)) / 1024
        print(f"  📄 {item} ({size:.1f} KB)")
    else:
        print(f"  📁 {item}/")
