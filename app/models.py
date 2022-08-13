from sqlalchemy.sql.functions import current_timestamp

from app.app import db, celery_instance
from celery.result import AsyncResult
from app.db_controller.controller import AbsModel


class DateTimeMixin:
    created_at = db.Column(db.DateTime, default=current_timestamp())
    updated_at = db.Column(db.DateTime, default=current_timestamp())
    closed_at = db.Column(db.DateTime)


class DigitalUsers(AbsModel):
    __tablename__ = 'digital_user'

    socnet_id = db.Column(db.Text(), index=True, unique=True)  # user nickname
    socnet_name = db.Column(db.Text(), index=True, nullable=False)  # twitter, telegram etc.
    register_date = db.Column(db.DateTime, default=current_timestamp())
    account_status = db.Column(db.String(), nullable=False)  # open, closed, deleted
    last_visited = db.Column(db.DateTime(), nullable=True)  # time of the last scan by crawler

    # Declare one-to-many relationships
    posts = db.relationship('Posts', backref=db.backref(
                                          'digital_users'))
    task = db.relationship('Task', backref=db.backref("digital_users"))

    # Declare one-to-one relationships
    suicide_rating = db.relationship('DuserRisk', backref=db.backref("digital_users"))
    # ruser_id = db.Column(db.Integer(), db.ForeignKey('real_user.id'))

    def __repr__(self):
        return f'<User {self.socnet_id}>'

    @property
    def link(self):
        return f'https://{self.socnet_name}.com/{self.socnet_id}'


class Posts(AbsModel):
    __tablename__ = 'post'

    user_id = db.Column(db.Integer(), db.ForeignKey('digital_user.id'))
    text = db.Column(db.Text(), index=True)
    is_retweeted = db.Column(db.Boolean(), nullable=True)
    creation_date = db.Column(db.DateTime, default=current_timestamp())
    #annotation = db.Column(db.Integer(), nullable=True)
    annotation = db.relationship('PostAnnot', backref=db.backref("post"))

    def __repr__(self):
        return f'<Post {self.id}>'


class Task(AbsModel):
    __tablename__ = "task"

    user_id = db.Column(db.Integer(), db.ForeignKey("digital_user.id"))
    task_id = db.Column(db.String())
    creation_date = db.Column(db.DateTime, default=current_timestamp())
    is_done = db.Column(db.Boolean())
    
    @property
    def get_last_job(self, user_id):
        # TODO:
        # add sorting by time
        return AsyncResult(self.get({"user_id": user_id}), app=celery_instance)

# class Multimedia(Base):
#     __tablename__ = 'multimedia'
#     id = db.Column(db.Integer(), primary_key=True, unique=True)
#     post_id = db.Column(db.Integer(), db.ForeignKey('posts.id'))
#     type = db.Column(db.Text())
#     path = db.Column(db.Text())
#
#     def __repr__(self) -> str:
#         return f"Multimedia: id:{self.id}, {self.path}"


class PostAnnot(AbsModel):
    __tablename__ = "post_annot"

    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))
    attr_by_model = db.Column(db.String())
    attr_by_human = db.Column(db.String())

    def __repr__(self):
        return f'<PostAnnot {self.id}>'


class DuserRisk(AbsModel):
    __tablename__ = "duser_risk"

    duser_id = db.Column(db.Integer(), db.ForeignKey('digital_user.id'))
    model_risk_estimation = db.Column(db.Integer())
    human_risk_estimation = db.Column(db.Integer())

    def __repr__(self):
            return f'<DuserRisk {self.id}>'











