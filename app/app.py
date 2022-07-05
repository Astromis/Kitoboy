import os
import sys
import logging
# from celery import Celery
from flask import Flask
#from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
#from flask_restplus import Api
from flask_script import Manager
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from dev_config import DevelopmentConfig as config
from flask import render_template

# LOG_DIR = os.path.join(os.path.dirname(root.__file__), "logs", "errors.log")
#
#
# def get_logger(name=__file__, file=LOG_DIR, encoding='utf-8'):
#     log = logging.getLogger(name)
#     log.setLevel(logging.ERROR)
#
#     formatter = logging.Formatter(
#         '[%(asctime)s] %(levelname)-8s %(message)s')
#
#     fh = logging.FileHandler(file, encoding=encoding)
#     fh.setFormatter(formatter)
#     log.addHandler(fh)
#
#     sh = logging.StreamHandler(stream=sys.stdout)
#     sh.setFormatter(formatter)
#     log.addHandler(sh)
#
#     return log
#

app = Flask(__name__)
app.config.from_object(config)

# @app.route('/')
# def home():
#     return render_template('index.html')

# jwt = JWTManager(app)
#
# bcrypt = Bcrypt(app)
# cache = Cache(app)
# celery = Celery('tasks', broker=app.config['CELERY_BROKER_URL'],
#                 backend=app.config['CELERY_RESULT_BACKEND'])
# celery.conf.update(app.config)

# lm = LoginManager(app)
# lm.login_view = '/labeling_auth/login'

db = SQLAlchemy(app)
ma = Marshmallow(app)
#api = Api(app)
# params_parser = api.parser()

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

CORS(app)
