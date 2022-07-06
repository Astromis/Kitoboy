import json
import os
import random
# from flask_bcrypt import Bcrypt

from app.app import manager
from app.models import *
# from app.tasks_manager_api.models import *
# from app.datasets.models import *
# from app.common_entities.models import *


# def multi_add(file_path, arg, params, table):
#     if file_path is None:
#         for param in params.split(','):
#             table.create(**{arg: param})
#     else:
#         file_params(file_path, table)


import json
import os
import random
# from flask_bcrypt import Bcrypt

# from app.app import manager
# from app.auth_api.models import *
# from app.tasks_manager_api.models import *
# from app.datasets.models import *
# from app.common_entities.models import *


def file_params(file_path, table):
    with open(file_path, 'r') as f:
        data = json.load(f)
    for sample in data:
        table.create(**sample)


def multi_add(file_path, arg, params, table):
    if file_path is None:
        for param in params.split(','):
            table.create(**{arg: param})
    else:
        file_params(file_path, table)


@manager.command
def drop_db():
    db.drop_all()


@manager.command
def create_db():
    db.create_all()


@manager.option('-f', '--file', help='path to file')
def create_digital_users(file):
    """Creates users from file"""
    with open(file, 'r') as f:
        data = json.load(f)
    for user in data:
        DigitalUsers.create(**user)


@manager.command
def create_posts():
    # with open(file, 'r') as f:
    #     data = json.load(f)
    # for user in data:
    #     DigitalUser.create(**user)
    # for user in DigitalUsers.get_all():
    #     posts = [Posts.create(user_id=user.id, text= f'Test post {i} {user.socnet_id}') for i in range(5)]
    #     #t est_text = f'Test post {i} for {user.id}'
    #     print(posts)
    #
    #     user.update(posts=posts)
    #     #user.posts.append(posts[0])
    for user in DigitalUsers.get_all():
        print(user, user.id)
        print(user.posts)

    print('!!!!')
    return


if __name__ == '__main__':
    manager.run()
