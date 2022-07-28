from datetime import datetime
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import re
import matplotlib.pyplot as plt
import seaborn as sns

import nltk
nltk.download('vader_lexicon')

def date_time(df):
    df['tweet_date'] = df['tweet_dt'].apply(lambda x: datetime.strptime(x,'%Y-%m-%d'))
    df['dt'] = pd.to_datetime(df['tweet_date'])
    return df


def sia_analysis(df):

    sid = SIA()
    df['sentiments'] = df['body'].apply(lambda x: sid.polarity_scores(' '.join(re.findall(r'\w+',x.lower()))))
    df['Positive Sentiment'] = df['sentiments'].apply(lambda x: x['pos']+1*(10**-6))
    df['Neutral Sentiment']= df['sentiments'].apply(lambda x: x['neu']+1*(10**-6))
    df['Negative Sentiment']= df['sentiments'].apply(lambda x: x['neg']+1*(10**-6))

    df.drop(columns=['sentiments'],inplace=True)

    return df

def plot_sentiments(df, title):

    plt.figure(figsize=(20,10))
    plt.title('Distribution Of Sentiments Across Our Tweets about '+ title,fontsize=19,fontweight='bold')
    sns.kdeplot(df['Negative Sentiment'],bw_method=0.1,label = 'Negative')
    sns.kdeplot(df['Positive Sentiment'],bw_method=0.1,label = 'Positive')
    sns.kdeplot(df['Neutral Sentiment'],bw_method=0.1,label = 'Neutral')
    plt.xlabel('Sentiment scores')
    plt.legend()
    plt.show()



def create_df_sent(df):


    df_original = df.copy()
    # Saving the maximum values between the three sentiments and their respective class
    df_sentiment = pd.DataFrame()
    df_sentiment['Max_SentimentCol'] = df[['Negative Sentiment','Positive Sentiment','Neutral Sentiment']].idxmax(axis=1)
    df_sentiment['Max_SentimentValue'] = df[['Negative Sentiment','Positive Sentiment','Neutral Sentiment']].max(axis=1)
    # df_sentiment = df_sentiment.drop(['Negative Sentiment','Positive Sentiment','Neutral Sentiment'], axis=1)


    # Union of new dataframe and original one
    # df_new = df_sentiment.join(df_original)
    return df_sentiment


#TRASFORMANDO IN DATE LE STRINGHE PER POTER RAGGRUPARE LA MEDIA DEI VALORI MASSIMI DI SENTIMENT SCORE PER CATEGORIA (POS,NEG,NEUTRAL) E MESE
def plot_sent_distribution(df_new, title = 'no-title', no_plot = True):

    list_YM = [i.split(" ")[0][:-3] for i in  list(df_new['tweet_dt'])]
    list_Year = [i.split(" ")[0][0:4] for i in  list(df_new['tweet_dt'])]
    list_Month = [i.split(" ")[0][5:7] for i in  list(df_new['tweet_dt'])]

    df_new['YM'] = list_YM
    df_new['Year'] = list_Year
    df_new['Month'] = list_Month

    #create a monthly dataframe
    df_mean = df_new.groupby(['Max_SentimentCol', 'YM', 'Year', 'Month']).mean()
    df_mean = df_mean[['Max_SentimentValue']].reset_index()
    df_mean.sort_values(by='YM',inplace=True)

    if not no_plot:
        sns.set(rc={'figure.figsize':(40,10)})
        ax = sns.lineplot(data=df_mean, x = 'YM', y='Max_SentimentValue',hue='Max_SentimentCol',palette='viridis',legend='full',lw=3)
        xticks = ax.xaxis.get_major_ticks()
        for i in range(len(xticks)):
            if i%2==1:
                xticks[i].set_visible(False)

        plt.legend(bbox_to_anchor=(1, 1))
        plt.title('Distribution of the sentiment score over time by ' + title)
        plt.ylabel('Mean Sentiment Score')
        plt.xlabel('Year-Month')
        plt.xticks(rotation=45)
        plt.show()

    return