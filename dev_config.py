import os
from datetime import timedelta


class Config:
    SECRET_KEY = '2b$12$ISYJTUMki6kpmF3wC5zQt'
    JWT_SECRET_KEY = '2sdfgGGYJTUMsSFki6kpmF3wC5zQ@#$t'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)
    DEBUG = False
    # URL_PREFIX_AUTH_API = '/labeling_auth'
    # URL_PREFIX_TASK_MANAGER_API = '/labeling_tm'
    #
    # AZURE = os.getenv('AZURE', 'True')
    # STORAGE_ACCOUNT_NAME = os.getenv('STORAGE_ACCOUNT_NAME', 'mtsdatalake')
    # STORAGE_ACCOUNT_KEY = os.getenv('STORAGE_ACCOUNT_KEY',
    #                                 'qq+a/VyO569Kt0k1WH551wJl9+jt3R7Cqu144HKQ7GhR8P9M8poYggw4ANJM+BWQWu3NWcgDp0RS1WDJF8QM0g==')
    # AZURE_URL = os.getenv('AZURE_URL',
    #                       'https://mtsadm7878.documents.azure.com:443/')
    # AZURE_KEY = os.getenv('AZURE_KEY',
    #                       'fMg5yLe16LBWnH7BA2Rutp05EE4WT55m0dkAePwUgJPiyYFJtdSBLlKWjBQTAFxO2TrMMDyS0sOLkum6GN4lmQ==')
    # AZ_FILE_SYSTEM = os.getenv('AZ_FILE_SYSTEM', 'labeling')
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL',
                                       'redis://localhost:6379'),
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND',
                                           'redis://localhost:6379')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    LABELING_DB_NAME = 'labeling_db'
    DB_USER = os.getenv('POSTGRES_USER', 'label_it')
    DB_PASS = os.getenv('POSTGRES_PASSWORD', '12345')
    DB_SERVICE = os.getenv('POSTGRES_SERVICE', 'localhost')
    DB_PORT = os.getenv('POSTGRES_PORT', '5432')
    COMMON_DATABASE_PATH = f'postgresql://{DB_USER}:{DB_PASS}@{DB_SERVICE}:{DB_PORT}'

    SQLALCHEMY_DATABASE_URI = f'{COMMON_DATABASE_PATH}/{LABELING_DB_NAME}'
