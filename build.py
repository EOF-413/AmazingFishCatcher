import os
import sys
import subprocess

print("=" * 50)
print("AmazingStreetCleaner - Сборка .exe")
print("=" * 50)

for folder in ['dist', 'build']:
    if os.path.exists(folder):
        import shutil
        shutil.rmtree(folder)
        print(f"[CLEAN] Удалена папка {folder}")

print("[BUILD] Запуск сборки...")
cmd = [
    sys.executable, '-m', 'PyInstaller',
    '--onefile',
    '--noconsole',
    '--name=AmazingStreetCleaner',
    '--add-data=templates;templates',
    '--hidden-import=PyQt5',
    '--hidden-import=cv2',
    '--hidden-import=numpy',
    '--hidden-import=PIL',
    '--hidden-import=pynput',
    '--clean',
    '--noconfirm',
    'main.py'
]

if os.path.exists('icon.ico'):
    cmd.insert(4, '--icon=icon.ico')
    print("[OK] Иконка найдена")

subprocess.run(cmd)

print("\n" + "=" * 50)
if os.path.exists('dist/AmazingStreetCleaner.exe'):
    size = os.path.getsize('dist/AmazingStreetCleaner.exe') / (1024 * 1024)
    print("✅ Сборка завершена!")
    print(f"📁 Размер: {size:.2f} MB")
    print("📁 dist/AmazingStreetCleaner.exe")
else:
    print("❌ Сборка не удалась")
print("=" * 50)

input("\nНажмите Enter для выхода...")
