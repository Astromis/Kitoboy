from datetime import date
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base

engine = db.create_engine("sqlite:///scraper.db")

Base = declarative_base()

class Posts(Base):
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    text = db.Column(db.Text())
    is_reposted = db.Column(db.Boolean())
    datetime = db.Column(db.DateTime())
    multimedia = db.orm.relationship("Multimedia", backref="post")
    annotation = db.Column(db.Integer())

    def __repr__(self) -> str:
        return f"Post: id:{self.id}, '{self.text}', {self.datetime}"


class Users(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    user_tag = db.Column(db.Text(), )
    socnet_type = db.Column(db.Text())
    suicide_rating = db.Column(db.Integer)
    last_visited = db.Column(db.DateTime())
    is_exists = db.Column(db.Boolean())
    posts = db.orm.relationship("Posts", backref="user")

    def __repr__(self) -> str:
        return f"User: id:{self.id}, {self.user_tag}, {self.last_visited}"
    

class Multimedia(Base):
    __tablename__ = 'multimedia'
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    post_id = db.Column(db.Integer(), db.ForeignKey('posts.id'))
    type = db.Column(db.Text())
    path = db.Column(db.Text())

    def __repr__(self) -> str:
        return f"Multimedia: id:{self.id}, {self.path}"

# Base.metadata.create_all(engine)