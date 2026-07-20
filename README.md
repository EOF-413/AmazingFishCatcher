# 🚀 AmazingFishCatcher

<div align="center">

[![Version](https://img.shields.io/badge/version-1.0.2-blue.svg)](https://github.com/EOF-413/AmazingStreetCleaner)
[![Python](https://img.shields.io/badge/python-3.11.0-yellow.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Windows](https://img.shields.io/badge/platform-Windows-blue.svg)](https://www.microsoft.com/windows)

**Автоматическое нажатие клавиш по шаблонам на экране**

</div>

---

## 📋 Описание

AmazingFishCatcher - программа для автоматического нажатия клавиш на основе распознавания шаблонов на экране. Создана для удобной работы на проекте AMAZING ONLINE, где требуется автоматизация повторяющихся действий.

### ✨ Возможности

- 🎯 **Распознавание шаблонов** - использует OpenCV для поиска изображений на экране
- ⌨️ **Автоматическое нажатие клавиш** - через библиотеку pynput
- ⚡ **Высокая производительность** - оптимизированная работа с процессором
- 🎨 **Современный интерфейс** - тёмная тема на PyQt5
- 🔧 **Гибкие настройки** - все параметры можно менять в реальном времени
- 💾 **Сохранение настроек** - конфиг хранится в `%AppData%/EOF-413/AFC`
- 🖥️ **Глобальный хоткей** - F9 для старта/остановки
- 📊 **Логирование** - цветовой лог для отслеживания действий

---

## 📦 Установка

### Способ 1: Установка из установщика (рекомендуется)

1. Скачайте установщик `AFC.exe`
2. Запустите установщик и следуйте инструкциям
3. Запустите программу через ярлык на рабочем столе или в меню Пуск

### Способ 2: Запуск из исходников

```bash
# Клонирование репозитория
git clone https://github.com/EOF-413/AmazingFishCatcher.git

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
