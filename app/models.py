# from app.auth_api.models import User
# from app.datasets.models import Dataset
from sqlalchemy.sql.functions import current_timestamp

from app.app import db, ma
from app.db_controller.controller import AbsModel


# class GuidelineSchema(ma.Schema):
#     class Meta:
#         fields = ('id', 'title', 'content', 'author_login')
#
#
# class BaseSchema(ma.Schema):
#     class Meta:
#         fields = ('id', 'name')
#
#
# class ProductSchema(ma.Schema):
#     class Meta:
#      LINE_SCHEMAS = GuidelineSchema()
# GUIDELINES_SCHEMA = GuidelineSchema(many=True)
#
# BASE_SCHEMA = BaseSchema(many=True)
#
# PRODUCT_SCHEMA = ProductSchema()
# PRODUCTS_SCHEMA = ProductSchema(many=True)
#    fields = ('id', 'name', 'project_types')
#
#
# GUIDELINE_SCHEMAS = GuidelineSchema()
# GUIDELINES_SCHEMA = GuidelineSchema(many=True)
#
# BASE_SCHEMA = BaseSchema(many=True)
#
# PRODUCT_SCHEMA = ProductSchema()
# PRODUCTS_SCHEMA = ProductSchema(many=True)


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





# class Status(AbsModel):
#     __tablename__ = 'status'
#
#     name = db.Column(db.String(64), nullable=False, unique=True)
#
#     def __repr__(self):
#         return self.name + f' {self.id}'
#
#
# class Priority(AbsModel):
#     __tablename__ = 'priority'
#
#     name = db.Column(db.String(64), nullable=False, unique=True)
#
#     def __repr__(self):
#         return self.name
#
#
# class LabelRgb(AbsModel):
#     __tablename__ = 'label_rgb'
#     __table_args__ = (
#         db.UniqueConstraint('label_id', 'rgb_code'),)
#
#     label_id = db.Column(db.Integer, db.ForeignKey('label.id'))
#     rgb_code = db.Column(db.String(7), nullable=False, unique=True)
#
#     @property
#     def label_rgb_info(self):
#         label = Label.get(id=self.label_id)
#         return {
#             'id': self.id,
#             'label_ru': label.ru_name,
#             'label_en': label.en_name,
#             'color': self.rgb_code,
#             'product_id': label.product_id
#         }
#
#
# class Label(DateTimeMixin, AbsModel):
#     """
#     Model contains labels
#     relationships many to many
#     """
#     __tablename__ = 'label'
#     ru_name = db.Column(db.String(64), nullable=False, unique=True)
#     en_name = db.Column(db.String(64), nullable=False, unique=True)
#     author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     product_id = db.Column(db.Integer, db.ForeignKey('product_category.id'),
#                            nullable=True)
#
#     def __repr__(self):
#         return self.en_name
#
#
# class ProductCategory(AbsModel):
#     __tablename__ = 'product_category'
#     name = db.Column(db.String(64), unique=True, nullable=False)
#
#     def __repr__(self):
#         return self.name
#
#     @property
#     def project_types(self):
#         return Dataset.get_allowed_types(self.id)







# from datetime import date
# import sqlalchemy as db
# from sqlalchemy.ext.declarative import declarative_base
#
# engine = db.create_engine("sqlite:///scraper.db")
#
# Base = declarative_base()
#
# class Posts(Base):
#     __tablename__ = 'posts'
#     id = db.Column(db.Integer(), primary_key=True, unique=True)
#     user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
#     text = db.Column(db.Text())
#     is_reposted = db.Column(db.Boolean())
#     datetime = db.Column(db.DateTime())
#     multimedia = db.orm.relationship("Multimedia", backref="post")
#     annotation = db.Column(db.Integer())
#
#     def __repr__(self) -> str:
#         return f"Post: id:{self.id}, '{self.text}', {self.datetime}"
#
#
# class Users(Base):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer(), primary_key=True, unique=True)
#     user_tag = db.Column(db.Text(), )
#     socnet_type = db.Column(db.Text())
#     suicide_rating = db.Column(db.Integer)
#     last_visited = db.Column(db.DateTime())
#     is_exists = db.Column(db.Boolean())
#     posts = db.orm.relationship("Posts", backref="user")
#
#     def __repr__(self) -> str:
#         return f"User: id:{self.id}, {self.user_tag}, {self.last_visited}"
#
#
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
# Base.metadata.create_all(engine)