# all the imports
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
from utils import predict_suicidal_signals
from twitter_scrapper import get_tweeter_user
from subprocess import Popen

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

OUTER_STATS = {}

app = Flask(__name__)
app.config.from_object(__name__)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)
    
@app.route('/', methods=['GET', 'POST'])
def get_link():
    if request.method == 'POST':
        pass
        
        input_type = request.form['input_type']
        
        if input_type == "Twitter":
            df = get_tweeter_user(request.form["user_url"])
        elif input_type == "Telegram":
            char_url = request.form["user_url"]
            p = Popen(["python", "telegram_scrapper.py", char_url], shell=False)
            p.communicate()
            df = pd.read_csv(f"data/telegram_chat_{char_url}", sep="|")
       
        #df.to_csv("test.csv", sep="|")
        # df = pd.read_csv("test.csv", sep="|")
        df.dropna(inplace=True)
        sent_label, sent_score = get_sentiments(df.text.tolist())
        suicide_label = predict_suicidal_signals(df.text.tolist())
        df["sentiment"] = sent_label
        df["score"] = sent_score
        df["suicide_label"] = suicide_label
        df = df[~df.sentiment.isin(["skip", "speech"])]
        df.to_csv("data/debug.csv", sep="|")
        # OUTER_STATS["emotion_coef"] = get_sentiment_dynamic(df)
        # stats = get_common_stats(df, OUTER_STATS)
        neg_text = df[(df.score > 0.75)& (df.sentiment == "negative")].text.tolist()
        pos_text = df[(df.score > 0.75)& (df.sentiment == "positive")].text.tolist()
        suicidal_signals = df[df.suicide_label == 1].text.tolist()
        other_data = [] #extract_data(df.text)
        if input_type == "Twitter":
            return render_template("userpage.html", sentiment_dynamic = Path("static/img/test.png"), neg_text=neg_text, pos_text=pos_text, other_data=other_data, suicidal_signals=suicidal_signals) 
        else:
            return render_template("userpage_telegram.html", groped_users=df)

    else:
        return '''
        <!doctype html>
        <title>Китобой</title>
        <h1>Введите Twitter ссылку</h1>
        <form action="" method=post >

        <input type="radio" id="input_type_1"
            name="input_type" value="Telegram">
        <label for="input_type">Telegram</label>

        <input type="radio" id="input_type_2"
            name="input_type" value="Twitter">
        <label for="input_type">Twitter</label>
        <p><input type=text name=user_url>
            <input type=submit value=Scan>
        </form>
        '''
    
if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=DEBUG)
