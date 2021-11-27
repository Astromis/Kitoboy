# all the imports
import sqlite3
import os

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired


from flask import send_from_directory

import pandas as pd
import pymorphy2
import json
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from utils import get_sentiments
from utils import get_sentiment_dynamic
from utils import get_common_stats
from utils import extract_data
from twitter_scrapper import get_tweeter_user
#from models import User

# configuration
from config import Config


OUTER_STATS = {}

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#app.config.from_envvar('FLASKR_SETTINGS', silent=True)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

class Users(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    user_id = db.Column(db.Text(), index=True, unique=True)
    socnet_name = db.Column(db.Text(), index=True)
    is_collected = db.Column(db.Boolean(), default=False)
    suicide_rating = db.Column(db.Integer())
    posts = db.relationship('Posts', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.user_id)


class Posts(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Text(), db.ForeignKey('users.user_id'))
    text = db.Column(db.Text(), index=True)
    is_retweeted = db.Column(db.Boolean())
    date = db.Column(db.Text())
    annotation = db.Column(db.Integer())

    def __repr__(self):
        return '<Post {}>'.format(self.id)


class PhotoForm(FlaskForm):
    file = FileField(validators=[FileRequired()])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in Config.ALLOWED_EXTENSIONS
    
""" @app.route('/', methods=['GET', 'POST'])
def get_link():
    if request.method == 'POST':
        df = get_tweeter_user(request.form["user_url"])
        df.to_csv("test.csv", sep="|")
        #df = pd.read_csv("test.csv", sep="|")
        df.dropna(inplace=True)
        sent_label, sent_score = get_sentiments(df.text.tolist())
        
        df["sentiment"] = sent_label
        df["score"] = sent_score
        df = df[~df.sentiment.isin(["skip", "speech"])]
        OUTER_STATS["emotion_coef"] = get_sentiment_dynamic(df)
        stats = get_common_stats(df, OUTER_STATS)
        neg_text = df[(df.score > 0.75)& (df.sentiment == "negative")].text.tolist()
        pos_text = df[(df.score > 0.75)& (df.sentiment == "positive")].text.tolist()
        other_data = extract_data(df.text)
        return render_template("userpage.html", sentiment_dynamic = Path("static/img/test.png"), neg_text=neg_text, pos_text=pos_text, stats=stats, other_data=other_data) 

    else:
        return render_template('main.html') """

@app.route('/', methods=['GET', 'POST'])
def index():
    form = PhotoForm()
    if form.validate_on_submit():
        f = form.file.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            'data', filename
        ))
        df = pd.read_csv(f"data/{filename}", sep='|')
        for i, r in df.iterrows():
            new_user = Users(id=1, user_id=r.link.split("/")[-1], socnet_name="Twitter", suicide_rating=r.label)
            db.session.add(new_user)
        db.session.commit()

    return render_template("index.html",form=form)

@app.route("/users/")
def users():
        users = Users.query.filter_by(socnet_name='Twitter').all()
        return render_template('show_users.html', users_list=users)

@app.route("/user_posts/<user>")
def user_posts(user):
    posts = Posts.query.filter_by(user_id=user).all()
    return render_template('show_posts.html', post_list=posts)

    
if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=Config.DEBUG)

'''
        <!doctype html>
        <title>Китобой</title>
        <h1>Введите Twitter ссылку</h1>
        <form action="" method=post >
        <p><input type=text name=user_url>
            <input type=submit value=Upload>
        </form>
        '''