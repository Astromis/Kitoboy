from datetime import date
from app import db

class RealUser(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    middle_name = db.Column(db.String())
    age = db.Column(db.String())
    from_country = db.Column(db.String())
    study_level = db.Column(db.String())
    status = db.Column(db.String())
    is_volunteer = db.Column(db.Boolean())
    is_supervisor = db.Column(db.Boolean())
    #supervised_by = db.Column(db.String())
    associated_social_user = db.relationship("DigitalUser", backref="digit_user", lazy='dynamic')
    logs = db.relationship("Log", backref="logs", lazy='dynamic')
    #address = db.relationship("Address", backref="address", lazy='dynamic')

class VolunteeredBy(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('real_user.id'))
    volunteer_id = db.Column(db.Integer(), db.ForeignKey('real_user.id'))
    # is_assigned = db.Column(db.Boolean())

class SupervisedBy(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('real_user.id'))
    supervisor_id = db.Column(db.Integer(), db.ForeignKey('real_user.id'))
    datetime = db.Column(db.DateTime())
    comment = db.Column(db.String())

class TakenActions(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('real_user.id'))
    datetime = db.Column(db.DateTime())
    event = db.Column(db.DateTime())
    volunteer_id = db.Column(db.String())
    comment = db.Column(db.String())

class Address(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('real_user.id'))
    address = db.Column(db.String())

class Phone(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('real_user.id'))
    phone_number = db.Column(db.String())

class Log(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('real_user.id'))
    log_text = db.Column(db.Text())
    #datetime = db.Column(db.DateTime())

# class Files
# class Relatives

class DigitalUser(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    associated_real_user =  db.Column(db.Integer(), db.ForeignKey('real_user.id'))
    socnet_id = db.Column(db.Text(), index=True, unique=True)
    socnet_name = db.Column(db.Text(), index=True)
    is_collected = db.Column(db.Boolean())
    account_status = db.Column(db.String()) # open, closed, deleted
    #suicide_rating = db.Column(db.String())
    last_visited = db.Column(db.DateTime())
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    suicide_rating = db.relationship('SocnetRisk', backref='suicide_rate', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.user_account)

class SocnetRelationship(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    src_id =  db.Column(db.Integer(), db.ForeignKey('digital_user.id'))
    trg_id =  db.Column(db.Integer(), db.ForeignKey('digital_user.id'))
    relation_type = db.Column(db.String())

class SocnetRisk(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    socnet_id =  db.Column(db.Integer(), db.ForeignKey('digital_user.id'))
    model_risk_estimation = db.Column(db.String())
    human_risk_estimation = db.Column(db.String())


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('digital_user.id'))
    text = db.Column(db.Text(), index=True)
    is_retweeted = db.Column(db.Boolean())
    datetime = db.Column(db.DateTime())
    annotation = db.Column(db.Integer())

    def __repr__(self):
        return '<Post {}>'.format(self.id)

class PostAttrs(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))
    attr_by_model =  db.Column(db.String())
    attr_by_human =  db.Column(db.String())

class PostReplies(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    base_msg_id = db.Column(db.Integer(), db.ForeignKey('post.id'))
    reply_msg_id = db.Column(db.Integer(), db.ForeignKey('post.id'))

class PostInteraction(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('digital_user.id'))
    action_type = db.Column(db.String())