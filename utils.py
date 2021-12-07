from nltk import word_tokenize
import pymorphy2


import pandas as pd
from dostoevsky.models import FastTextSocialNetworkModel
from dostoevsky.tokenization import RegexTokenizer
#from matplotlib import pyplot as plt
import numpy as np
import re
from time import sleep

regex = [ ("[OLD]" ,re.compile(r"мне ([6-9])|([0-9]{2,2}) (лет|год)?") ), 
           ("[BANK]", re.compile(r"([0-9]{4,4}[ ]?){4,4}")),
           ("[TELE]", re.compile(r"^((\+?[0-9]{1,3})[\- ]?)?(\(?\d{3,4}\)?[\- ]?)?[\d\- ]{5,10}$"))]

towns = pd.read_csv("data/russian_town_list.csv", sep="|", header=None)
with open("data/russian_names_dict.txt") as f:
    names = f.read().lower().split() 


towns = towns[0].to_list()

morph = pymorphy2.MorphAnalyzer()
towns_extended = []
for t in towns:
    for form in ["gent", "loct"]:
        town = morph.parse(t.lower())[0]
        try:
            town = town.inflect({form}).word
        except:
            continue
        towns_extended.append(town)


for i in ["короче", "нее", "дна", "дне"]:
    towns_extended.pop(towns_extended.index(i)) 

morph = pymorphy2.MorphAnalyzer()
towns_extended = []
for t in towns:
    for form in ["gent", "loct"]:
        town = morph.parse(t.lower())[0]
        try:
            town = town.inflect({form}).word
        except:
            continue
        towns_extended.append(town)


for i in ["короче", "нее", "дна", "дне"]:
    towns_extended.pop(towns_extended.index(i)) 

def extract_data(texts:list):
    messages = []
    for m in texts:
        tokenized = word_tokenize(m.lower())
        for name in names:
            if name in tokenized:
                messages.append("[NAME] " + m)
        for name, r in regex:
            if r.search(m) != None:
                messages.append(f"{name} " + m)
        for t in towns_extended:
            if t in tokenized:
                messages.append("[TOWN] " + m)
    return messages

tokenizer = RegexTokenizer()
model = FastTextSocialNetworkModel(tokenizer=tokenizer)

def get_sentiments(text:list):
    for x in text:
        if not isinstance( x, str):
            print(x)
    
    results = model.predict(text, k=1)
    label = []
    score = []
    for x, y in list([list(x.items())[0] for x in results]):
        label.append(x)
        score.append(y)
    return label, score

def get_sentiment_dynamic(df):
    sent2score = {"neutral": 0, "negative": -1, "positive": 1}
    df["sent_num"] = df.sentiment.apply(lambda x: sent2score[x])
    df['date'] = pd.to_datetime(df['date']) - pd.to_timedelta(7, unit='d')
    df_ = df.groupby(['sentiment', pd.Grouper(key='date', freq='W-MON')])['sent_num'].sum().reset_index().sort_values('date')
    tm = df_.groupby("date").sum()
    #plt.figure(figsize=(15,5))
    xline = pd.date_range(start=tm.index[0], end=tm.index[-1], freq="7D")
    horiz_line_data = np.array([0 for i in range(len(xline))])
    #plt.plot(xline, horiz_line_data, 'r--')

    #plt.plot(tm.index, tm.sent_num)
    #plt.xticks(xline, xline.format(date_format="%Y-%m-%d"),rotation=45)
    #plt.grid()
    #plt.title("Эмоциональная динамика пользователя")
    #plt.ylabel('Кумулятивная эмоциональная оценка')
    #plt.xlabel('Время по неделям')
    #plt.savefig('static/img/test.png')
    #sleep(1)
    return df_.groupby("date").mean().sum()/len(df_)

def get_common_stats(df, outer):
    stats = {}
    stats["nickname"] = df[df.is_retweeted == False].nickname.tolist()[0]
    stats["all_posts"] = len(df)
    stats["neg_posts"] = len(df[ (df.sentiment == "negative")])
    stats["pos_posts"] = len(df[ (df.sentiment == "positive")])
    stats["erlier_post"] = df["date"].tolist()[-1].strftime('%Y-%m-%d')
    stats["emotion_coef"] = "{:.2f}".format(float(outer["emotion_coef"]))
    stats['persentage_of_retweets'] = "{:.2f}".format(len(df[df.is_retweeted==True]) / len(df))
    return stats
