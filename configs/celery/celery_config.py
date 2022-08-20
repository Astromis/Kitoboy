from celery.schedules import crontab


CELERY_IMPORTS = ('app.tasks')
CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'UTC'

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULE = {
    # Run task every minute
    'every-minute': {
        'task': 'app.tasks.task_1',
        'schedule': crontab(minute='*'),
    },
    # Run task every 2 minutes
    'every-two_minutes': {
        'task': 'app.tasks.task_2',
        'schedule': crontab(minute='*/2'),
    }
}