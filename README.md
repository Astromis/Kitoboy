# Китобой

Система предназначена для оценки эмоционального состояния пользователя по его постам в социальных сетях. Данная система используется волонтерами НКО "Молодежная Служба Безопастности".

# Функционал

* Краулинг текстовой информации из социальных сетей:
    * Twitter
* Оценка динамики эмоционального состояния
* Отображение позитивных и негативных постов пользователей
* Выдача сообщений, которе возможно содержат следующую информацию:
    * Имя
    * Возраст
    * Номер телефона
    * Номер банковской карты
    * Город
    
# Установка

Тестовый запуск производился на Ubuntu 16.04 с версией Python >=3.8

## Шаги установки

1. Скачать исходный код системы git clone ...
1. Установить зависимости командой `pip install -r requirements.txt`
2. Установить geckodriver
    1. Скачать `wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz`
    2. Распаковать `tar -xvzf geckodriver*`
    3. Сделать исполняемым файлом `chmod +x geckodriver`
    4. Добавить путь до файла в перереммную PATH `export PATH=$PATH:/path-to-extracted-file/`
3. Установить Mozilla Firefox командой `sudo apt install firefox`
4. Установить модель анализа сентиментов `python -m dostoevsky download fasttext-social-network-model`

# Запуск системы

Для запуска системы достаточно выполнить команду `python main.py`. 
```
$ gunicorn --bind IP:PORT wsgi:app --timeout 600
```
IP - ip адрес приложения, например 127.0.0.1
PORT - желаемый порт, например 800

# Использование системы

Зайдя по домашнему адресу приложения, вам будет предложено ввести ссылку. В настоящее время поддерживается только Twitter. Скопируйте ссылку на профиль из адресной строки и вставьте ее. Ссылка на профиль будет выглядеть следующим образом "https://twitter.com/test_user_account". После чего, нажмите кнопку "Upload". После некоторого ожидания, откроется страница с информацией о пользователе. В разделе "Общая информация" собраны основные атрибуты аккаунта, как ник, количество постов, начало активности. Далее, в разделах "Негативные посты" и "Позитивные посты" будут отражены посты соответствующей полярности, в которых модель уверена больше чем 75 процентов. В разделе "Другая инфорация" будет представлена информация, которая сработала на правила. Правило обозначается тегом в начале сообщения

* \[NAME\] текст сообщения возможно содержит имя
* \[OLD\] текст сообщения возможно содержит возраст
* \[TOWN\] текст сообщения возможно содержит город
* \[TELE\] текст сообщения возможно содержит телефон
* \[BANK\] текст сообщения возможно содержит номер банковской карты
