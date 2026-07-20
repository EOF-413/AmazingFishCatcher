# 🚀 Amazing Fish Catcher

<div align="center">

[![Python](https://img.shields.io/badge/python-3.11.0-yellow.svg)](https://www.python.org/)
[![Windows](https://img.shields.io/badge/platform-Windows-blue.svg)](https://www.microsoft.com/windows)
[![Version](https://img.shields.io/badge/version-1.0.2-purple.svg)](https://github.com/EOF-413/AmazingStreetCleaner)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

</div>

## 📋 Описание

Amazing Fish Catcher - это программа для автоматического нажатия клавиш на работе уборщика улиц, проекта AMAZING ONLINE.

### ✨ Возможности

- 🖥️ **Глобальный хоткей** - F9 для старта/остановки.
- 🎨 **Современный интерфейс** - тёмная тема на PyQt5.
- 💾 **Сохранение настроек** - конфиг хранится в `%AppData%/EOF-413/AFC`.
- 🔧 **Гибкие настройки** - все параметры можно менять в реальном времени.
- 🎯 **Распознавание шаблонов** - использует OpenCV для поиска изображений на экране.

---

## 📦 Установка

### Способ 1: Установка из установщика (рекомендуется)

1. Скачайте установщик `AFC_Setup_X.Y.Z.exe`
2. Запустите установщик и следуйте инструкциям
3. Запустите программу через ярлык на рабочем столе или в меню Пуск

### Способ 2: Запуск из исходников

```bash
# Клонирование репозитория
git clone https://github.com/EOF-413/AmazingFishCatcher .git

# Вход в каталог
cd AmazingFishCatcher 

# Создание виртуального окружения
python -m venv venv

# Активация виртуального окружения
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Запуск программы
python main.py
