# all the imports
import sqlite3
import os

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from werkzeug.utils import secure_filename

from flask import send_from_directory

import pandas as pd
import pymorphy2
import json
from pathlib import Path

from utils import get_sentiments
from utils import get_sentiment_dynamic
from utils import get_common_stats
from utils import extract_data
from twitter_scrapper import get_tweeter_user

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'json'])


OUTER_STATS = {}

app = Flask(__name__)
app.config.from_object(__name__)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
""" 
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    else:
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form action="" method=post enctype=multipart/form-data>
        <p><input type=file name=file>
            <input type=submit value=Upload>
        </form>
        ''' """





    
@app.route('/', methods=['GET', 'POST'])
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
        return '''
        <!doctype html>
        <title>Китобой</title>
        <h1>Введите Twitter ссылку</h1>
        <form action="" method=post >
        <p><input type=text name=user_url>
            <input type=submit value=Upload>
        </form>
        '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    data = json.load(open(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
    total_len = sum([len(x) for x in list(data.values())])
    length = {x:len(y)/total_len for x,y in data.items()}
    filtered = {x:extract_data(y) for x,y in data.items()}
    return render_template('show_entries.html', dict_item=filtered, len=length)
    #return send_from_directory(app.config['UPLOAD_FOLDER'],
    #                           filename)

""" @app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)
    
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

    
def connect_db():
    return sqlite3.connect(app.config['DATABASE']) """
    
if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=DEBUG)
