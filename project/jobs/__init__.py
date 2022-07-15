"""__init__.py"""
import os
import yaml
from celery import Celery

base_dir = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(base_dir, 'config.yml')

with open(config_file, 'r', encoding="utf-8") as fp:
    try:
        config = yaml.safe_load(fp)
    except yaml.YAMLError as err:
        raise yaml.YAMLError(str(err))

broker = os.environ.get('CELERY_BROKER_URL', config.get('broker'))
backend = os.environ.get('CELERY_RESULT_BACKEND', config.get('backend'))
API_KEY = config.get('api_key')


def make_celery(app=None):
    '''
    celery factory: creating and returning a new celery instance
    :app: if None, the celery instance is "integrated" with the provided app
          typical example is flask web app etc.
    '''
    if app is None:
        celery = Celery(__name__, backend=backend, broker=broker)
    else:
        celery = Celery(
            app.import_name,
            broker=app.config['CELERY_BROKER_URL'],
            backend=app.config['CELERY_RESULT_BACKEND']
        )
        celery.conf.update(app.config)
        TaskBase = celery.Task

        class ContextTask(TaskBase): # pylint: disable=R0903
            '''Context for the task'''
            abstract = True

            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return TaskBase.__call__(self, *args, **kwargs)

        celery.Task = ContextTask

    return celery
