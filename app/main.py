# all the imports
import os
from re import L

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from werkzeug.utils import secure_filename

import pandas as pd
from pathlib import Path

""" from .utils import get_sentiments
from .utils import get_sentiment_dynamic
from .utils import get_common_stats
from .utils import extract_data
from .twitter_scrapper import get_tweeter_user """
from app import app, db
from app.models import DigitalUser, RealUser, SocnetRisk, Log, Post#, User
from app.forms import StatusForm, AddDigitalUser, AddLog, AddRealUser, SocnetUploadForm
from app.tables import SocNet_t

# configuration
from config import Config




""" def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in Config.ALLOWED_EXTENSIONS """
    
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
    users = RealUser.query.all()
    form = SocnetUploadForm()
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
            new_user = DigitalUser(user_account=r.link.split("/")[-1].strip(), socnet_name="Twitter") #, suicide_rating=r.label
            new_user.suicide_rating.human_risk_estimation = r.label
            db.session.add(new_user)
        db.session.commit()

    return render_template("index.html",form=form, users=users)

""" @app.route("/users/")
def users():
    page = request.args.get('page', 1, type=int)
    users = User.query.filter_by(socnet_name='Twitter').paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('users', page=users.next_num) \
        if users.has_next else None
    prev_url = url_for('users', page=users.prev_num) \
        if users.has_prev else None
    return render_template('show_users.html', users_list=users.items, rating_map=dict(Config.SUICIDAL_RATING), next_url=next_url, prev_url=prev_url) """

@app.route("/add_record", methods=['GET', 'POST'])
def add_record():
    form = AddRealUser()
    if form.validate_on_submit():
        user = RealUser(first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        middle_name=form.middle_name.data,
                        age=form.age.data,
                        from_country=form.from_country.data,
                        study_level=form.study_level.data,
                        status=form.status.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("add_user.html",form=form)

@app.route("/add_socnet/<id>", methods=['GET', 'POST'])
def add_socnet(id):
    form = AddDigitalUser()
    if form.validate_on_submit():
        user = DigitalUser(associated_real_user=form.id_real.data,
                        socnet_id=form.socnet_id.data,
                        socnet_name=form.socnet_name.data,
                        account_status=form.account_status.data)
        db.session.add(user)
        db.session.commit()
        db.session.add(SocnetRisk(socnet_id=user.id,
                                human_risk_estimation=form.suicide_rating.data))
        db.session.commit()
        return redirect(url_for("view_record", user=form.id_real.data, level='socnets'))
    return render_template("add_socnet.html",form=form, id=id)

@app.route('/edit_socnet/<int:id>', methods=['GET', 'POST'])
def edit_socnet(id):
    qry = DigitalUser.query.filter_by(id=id).first()

    if qry:
        form = AddDigitalUser(obj=qry)
        if request.method == 'POST' and form.validate():
            # save edits
            qry.account_status = form.account_status.data
            qry.suicide_rating.human_risk_estimation = form.suicide_rating.data
            db.session.commit()
            flash('Socnet updated successfully!')
            return redirect(url_for("view_record", user=form.id_real.data, level='socnets'))
        return render_template('add_socnet.html', form=form, id=id)
    else:
        return 'Error loading #{id}'.format(id=id)

@app.route('/delete_socnet/<int:id>', methods=['get'])
def delete_socnet(id):
    """
    delete the item in the database that matches the specified
    id in the url
    """
    qry = DigitalUser.query.filter_by(id=id).first()
    real_user_id = qry.associated_real_user
    #TODO: Admitting window
    #TODO: Forbidde deleteing if posts talbe is not emty
    if qry:
        # delete the item from the database
        db.session.delete(qry)
        db.session.commit()
        flash('Socnet deleted successfully!')
        return redirect(url_for("view_record", user=real_user_id, level='socnets'))
    else:
        return 'error deleting #{id}'.format(id=id)



@app.route("/add_log/<id>", methods=['GET', 'POST'])
def add_log(id):
    form = AddLog()
    if form.validate_on_submit():
        user = Log(user_id=form.id_real.data,
                    log_text=form.log_text.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("view_record", user=form.id_real.data, level='logs'))
    return render_template("add_log.html",form=form, id=id)

@app.route("/view_record/<user>/<level>", methods=['GET'])
def view_record(user, level):
    user = RealUser.query.filter_by(id=user).first()
    data = {}
    if level == 'socnets':
        data["digital_users_table"] = SocNet_t(user.associated_social_user.all())
        #TODO: related tables doesn't view
        #print( user.associated_social_user.first().suicide_rating.first().human_risk_estimation)
    elif level == "logs":
        data["logs"] = user.logs.all()
    return render_template("view_user.html",user=user, level=level, data=data)

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
    return render_template("edit_page.html",form=status_form, user=user, choices=Config.SUICIDAL_RATING)


@app.route("/user_posts/<id>")
def user_posts(id):
    posts = Post.query.filter_by(user_id=id).all()
    return render_template('show_posts.html', post_list=posts)

    
if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=Config.DEBUG)

