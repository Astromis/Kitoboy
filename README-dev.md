# HOW TO for Developers


##  Сборка docker-образа и запуск сервисов
Для работы с инструментами и сервисами, предоставляемыми в данном проекте, необходимо настроить программную среду выполнения. Для этого необходимо собрать docker-образ проекта и пользоваться всем функционалом из docker-контейнера.

Находясь в корне репозитория Kitoboy, выполнить команду:
```bash start.sh```


Результатом выполнения команды будет созданный docker-образ проекта и использующие его docker-контейнеры: 
- app (flask instance)
- db (postgres instance)
- brocker (redis instance)
- worker (celery worker)
- scheduler (celery beat)
- flower (tasks dashboard)


check on:
localhost:8000 (flask)
localhost:5555 (flower)


Для входа в контейнер базы данных выполнить команду:
```docker exec -it db psql -U test  -d kitoboy_db  --password```

(базовые команды для субд PostgreSQL см. https://www.postgresqltutorial.com/postgresql-administration/psql-commands/) 

Для открытия jupyter notebook в докер контейнере выполнить команду:

```docker exec app jupyter-notebook --allow-root --ip=0.0.0.0 --no-browser```
check on:
localhost:8888


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

