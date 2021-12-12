# all the imports
import os

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired#, 
from wtforms import SelectField, HiddenField, SubmitField, IntegerField

import pandas as pd
from pathlib import Path

#from wtforms.fields.simple import 

""" from .utils import get_sentiments
from .utils import get_sentiment_dynamic
from .utils import get_common_stats
from .utils import extract_data
from .twitter_scrapper import get_tweeter_user """
from app import app, db
from app.models import User

# configuration
from config import Config
SUICIDAL_RATING = [(0, "Normal"), (1, "Sus"), (2, "High")]

OUTER_STATS = {}

class PhotoForm(FlaskForm):
    file = FileField(validators=[FileRequired()])

class StatusForm(FlaskForm):
    id = HiddenField("id")
    status = SelectField("status", choices=SUICIDAL_RATING)
    submit = SubmitField('Update Record')


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
        if "link" not in df.columns  or "label" not in df.columns: #or "link" not in df.columns
            flash('Ivalid column format of file.')
            redirect(url_for('index'))
        for i, r in df.iterrows():
            new_user = User(user_account=r.link.split("/")[-1].strip(), socnet_name="Twitter", suicide_rating=r.label)
            db.session.add(new_user)
        db.session.commit()

    return render_template("index.html",form=form)

@app.route("/users/")
def users():
    page = request.args.get('page', 1, type=int)
    users = User.query.filter_by(socnet_name='Twitter').paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('users', page=users.next_num) \
        if users.has_next else None
    prev_url = url_for('users', page=users.prev_num) \
        if users.has_prev else None
    return render_template('show_users.html', users_list=users.items, rating_map=dict(SUICIDAL_RATING), next_url=next_url, prev_url=prev_url)

@app.route("/edit", methods=['GET', 'POST'])
def edit():
    # I'm not sure that this trick with id is a good solution
    id = request.args.get('id')
    status_form = StatusForm()
    user = User.query.filter(User.id == id).first()
    if status_form.is_submitted():
        user = User.query.filter(User.id == status_form.id.data).first()
        user.suicide_rating = status_form.status.data
        db.session.commit()
        return redirect(url_for("users"))
    return render_template("edit_page.html",form=status_form, user=user, choices=SUICIDAL_RATING)


@app.route("/user_posts/<user>")
def user_posts(user):
    posts = Post.query.filter_by(user_id=user).all()
    return render_template('show_posts.html', post_list=posts)

    
if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=Config.DEBUG)

