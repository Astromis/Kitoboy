
import pandas as pd
#from matplotlib import pyplot as plt
import numpy as np



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
    # emotional_coef = df_.groupby("date").mean().sum()/len(df_)

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


