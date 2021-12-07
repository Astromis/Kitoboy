from app import db

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    user_account = db.Column(db.Text(), index=True, unique=True)
    socnet_name = db.Column(db.Text(), index=True)
    is_collected = db.Column(db.Boolean())
    suicide_rating = db.Column(db.Integer())
    posts = db.relationship('Posts', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.user_id)

class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    text = db.Column(db.Text(), index=True)
    is_retweeted = db.Column(db.Boolean())
    datetime = db.Column(db.DateTime())
    annotation = db.Column(db.Integer())

    def __repr__(self):
        return '<Post {}>'.format(self.id)
