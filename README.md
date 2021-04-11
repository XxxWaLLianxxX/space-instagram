# Космический Инстаграм
Данная программа скачивает фотографии с Hubble и SpaceX и выкладывает их в ваш Instagram аккаунт. Полезно, если надо автоматически выложить много фотографий в профиль.
### Как установить
Чтобы бот начал выкладывать фотографии в аккаунт, надо в него зайти. Для начала, вам надо создать .env файл в корневой папке проекта. Затем, в самом файле вы должны указать ваш логин и пароль, примерно так (пробелов между знаком равно быть не должно):
```
LOGIN=вашлогин
PASSWORD=вашпароль
```
В коде уже указаны ключи для инстабота, вы просто написали значения для них в виде вашего логина и пароля.

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
### Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
