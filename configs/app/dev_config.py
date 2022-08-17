import os


class Config:
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DB_NAME = 'kitoboy_db'
    DB_USER = os.getenv('POSTGRES_USER', 'test')
    DB_PASS = os.getenv('POSTGRES_PASSWORD', '12345')
    DB_SERVICE = os.getenv('POSTGRES_SERVICE', 'localhost')
    DB_PORT = os.getenv('POSTGRES_PORT', '5432')
    COMMON_DATABASE_PATH = f'postgresql://{DB_USER}:{DB_PASS}@{DB_SERVICE}:{DB_PORT}'
    SQLALCHEMY_DATABASE_URI = f'{COMMON_DATABASE_PATH}/{DB_NAME}'

    # Redis URL configurations
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL',
                                       'redis://localhost:6379'),
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND',
                                           'redis://localhost:6379')


