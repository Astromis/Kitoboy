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


# Kitoboy Service

Структура проекта: 

Для поднятия контейнера с backend'ом необходимо выполнить:

1 sudo docker-compose up -d --build    # Поднятие контейнера
2 sudo docker exec kitoboy python3.6 db_manager.py create_db   # Создание таблиц в докере
3 sudo docker exec kitoboy ./scripts/./db_fill.sh dev | prod     # наполнение таблиц тестовыми данными:

check on:
localhost:8000


Для входа в бд в контейнере:
1 sudo docker exec -it ????? psql -U ?????  -d  ?????  --password


#3. sudo docker-compose -f docker-compose-db.yaml restart (применить pg_hba.conf)
#Чтобы изменить environment - нужно 1ую команду заменить на :
#sudo docker-compose -f docker-compose-db.yaml --env-file PATH up --build




# Migration Managment

В качестве основного механизма миграций используется [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/#)

Для инициализации таблиц при первом запуске необходимо выполнить команду:

  python db_manager.py create_db

В результате будут созданы таблицы в используемых БД на основании существующих моделей

Т.к. используется Flask-Migrate, то все его команды так же доступны из db_manager.py
Например:

  - Для изменения таблиц в БД на основании изменений модели необходимо выполнить

     python3 db_manager.py db migrate  "Изменение модели Users" - создается миграция с описанием
      и
     python3 db_manager.py db upgrade  - применяется миграция

  - Для того, чтобы откатить изменения до необходимой миграции необходимо выполнить

     python3 db_manager.py db downgrade <идентификатор ревизии revision к которой нужно откатиться>


# Set up pre-commit hook
- Install pre-commit package manager `pip install pre-commit`
- Install the git hook config (.pre-commit-config.yaml) at .git/hooks/pre-commit `pre-commit install`



