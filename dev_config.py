import os
from datetime import timedelta


class Config:
    SECRET_KEY = '2b$12$ISYJTUMki6kpmF3wC5zQt'
    JWT_SECRET_KEY = '2sdfgGGYJTUMsSFki6kpmF3wC5zQ@#$t'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)
    DEBUG = False
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL',
                                       'redis://localhost:6379'),
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND',
                                           'redis://localhost:6379')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DB_NAME = 'kitoboy_db'
    DB_USER = os.getenv('POSTGRES_USER', 'label_it')
    DB_PASS = os.getenv('POSTGRES_PASSWORD', '12345')
    DB_SERVICE = os.getenv('POSTGRES_SERVICE', 'localhost')
    DB_PORT = os.getenv('POSTGRES_PORT', '5432')
    COMMON_DATABASE_PATH = f'postgresql://{DB_USER}:{DB_PASS}@{DB_SERVICE}:{DB_PORT}'
    SQLALCHEMY_DATABASE_URI = f'{COMMON_DATABASE_PATH}/{DB_NAME}'
