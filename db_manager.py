import json


from app.app import manager
from app.models import *
from random import choice

POST_ANNOT = ["negative_enent", "enotional_state"]
USER_RISK = [0,1,2]


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

@manager.command
def create_post_annot():
    for post in Posts.get_all():
        annots = [PostAnnot.create(attr_by_model=choice(POST_ANNOT), attr_by_human=choice(POST_ANNOT))]
        post.update(annotation=annots)

    for post in Posts.get_all():
        print(f"{post} has annotations {post.annotation}")
    return

@manager.command
def fill_duser_risk():
    for user in DigitalUsers.get_all():
        risk = [DuserRisk.create(model_risk_estimation=choice(USER_RISK), human_risk_estimation=choice(USER_RISK))]
        user.update(suicide_rating=risk)

    for risk in DuserRisk.get_all():
        print(f"{risk.id} has estimation {risk.human_risk_estimation} and belongs to {risk.duser_id}")
        
    for user in DigitalUsers.get_all():
        print(f'{user}, {user.id} has risk {user.suicide_rating}')
    
    return


if __name__ == '__main__':
    manager.run()
