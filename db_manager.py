import json


from app.app import manager
from app.models import *


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
    for user in DigitalUsers.get_all():
        posts = [Posts.create(user_id=user.id, text=f'Test post {i} {user.socnet_id}') for i in range(5)]
        user.update(posts=posts)

    for user in DigitalUsers.get_all():
        print(f'{user}, {user.id} has posts {user.posts}')

    return


if __name__ == '__main__':
    manager.run()
