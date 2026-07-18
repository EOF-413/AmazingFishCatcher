# 🚀 AmazingStreetCleaner

<div align="center">

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/EOF-413/AmazingStreetCleaner)
[![Python](https://img.shields.io/badge/python-3.11.0-yellow.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Windows](https://img.shields.io/badge/platform-Windows-blue.svg)](https://www.microsoft.com/windows)

**Автоматическое нажатие клавиш по шаблонам на экране**

</div>

---

## 📋 Описание

AmazingStreetCleaner - это программа для автоматического нажатия клавиш на основе распознавания шаблонов на экране. 
Создана для удобной работы на проекте AMAZING ONLINE, где требуется автоматизация повторяющихся действий.

### ✨ Возможности

- 🎯 **Распознавание шаблонов** - использует OpenCV для поиска изображений на экране
- ⌨️ **Автоматическое нажатие клавиш** - через Win32 API

- ⚡ **Высокая скорость** - задержка менее 1мс
- 🚀 **Поддержка CUDA** - ускорение распознавания на видеокартах NVIDIA

- 🎨 **Современный интерфейс** - тёмная тема на PyQt5
- 🔧 **Гибкие настройки** - все параметры можно менять в реальном времени

---

## 📦 Установка

### 1. Клонирование репозитория

```bash
# Клонирование исходников
git clone https://github.com/EOF-413/AmazingStreetCleaner.git

# Вход в каталог
cd AmazingStreetCleaner

# Создание виртуального окружения
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
