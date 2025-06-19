# 🎥 YouTube Subtitle Finder

Приложение на Python с графическим интерфейсом для поиска субтитров к видео на YouTube. Пользователь указывает поисковую фразу и количество видео — программа найдёт видео по этой фразе и проверит наличие субтитров. Также доступна смена темы, языка интерфейса и возможность сохранить результаты.

## 📦 Возможности

- 🔎 Поиск видео по ключевой фразе с помощью `pytube`
- 🧠 Извлечение субтитров через `youtube-transcript-api`
- 🌐 Поддержка двух языков интерфейса: 🇷🇺 Русский и 🇬🇧 Английский
- 🎨 7 тем оформления: light, dark, solarized, dracula, monokai, matrix, blue
- ⏸ Возможность приостановить, возобновить или отменить поиск
- 💾 Сохранение результатов в `.txt` файл

## 🚀 Установка
1. Можно использовать как и .exe так и .py
2. Скачиваем [последний релиз](https://github.com/GeniusofAB/youtube-search-system/releases)
3. Запускаем .exe, если вам нужно .py - тогда:
4. Открываем командую строку или powershell
5. пишем: cd "C:/путь к файлу .py
6. пишем: python youtube_search_system.py (перед этим надо установить все зависимости)

## 📛 Зависимоти
```pip install pytube3, youtube-transcript-api```
## 📝 Лицензия

MIT License  
© 2025 GeniusofAB

Permission is hereby granted, free of charge, to any person obtaining a copy  
of this software and associated documentation files (the "Software"), to deal  
in the Software without restriction, including without limitation the rights  
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell  
copies of the Software, and to permit persons to whom the Software is  
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all  
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE  
SOFTWARE.
