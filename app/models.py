from sqlalchemy.sql.functions import current_timestamp

from app.app import db
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
    is_collected = db.Column(db.Boolean(), nullable=False)
    account_status = db.Column(db.String(), nullable=False)  # open, closed, deleted
    last_visited = db.Column(db.DateTime(), nullable=True)  # time of the last scan by crawler

    # Declare one-to-many relationship with Post model
    posts = db.relationship('Posts', backref=db.backref(
                                          'digital_users'))


    # suicide_rating = db.relationship('SocnetRisk', backref='suicide_rate', lazy='dynamic')
    # associated_real_user = db.Column(db.Integer(), db.ForeignKey('real_user.id'))

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
    annotation = db.Column(db.Integer(), nullable=True)

    def __repr__(self):
        return '<Post {}>'.format(self.id)


# class Multimedia(Base):
#     __tablename__ = 'multimedia'
#     id = db.Column(db.Integer(), primary_key=True, unique=True)
#     post_id = db.Column(db.Integer(), db.ForeignKey('posts.id'))
#     type = db.Column(db.Text())
#     path = db.Column(db.Text())
#
#     def __repr__(self) -> str:
#         return f"Multimedia: id:{self.id}, {self.path}"

#
# class PostAttrs(db.Model):
#     id = db.Column(db.Integer(), primary_key=True, unique=True)
#     post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))
#     attr_by_model = db.Column(db.String())
#     attr_by_human = db.Column(db.String())


# class SocnetRisk(db.Model):
#     id = db.Column(db.Integer(), primary_key=True, unique=True)
#     socnet_id = db.Column(db.Integer(), db.ForeignKey('digital_user.id'))
#     model_risk_estimation = db.Column(db.String())
#     human_risk_estimation = db.Column(db.String())











