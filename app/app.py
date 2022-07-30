from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_cors import CORS
from dev_config import DevelopmentConfig as config
from celery import Celery

celery_instance = Celery('app',
             broker='redis://localhost',
             backend='redis://localhost',
             include=['.tasks'])

celery_instance.conf.update(
    result_expires=3600,
)

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

CORS(app)
