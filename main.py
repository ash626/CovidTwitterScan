from twitterscraper import query_tweets_from_user
import datetime as dt
import json
import pandas as pd
from googletrans import Translator

def est_update(txt):
    test_list = ['update', 'stats', 'cases', 'outbreaks', 'confirmed', 'test', 'up to', 'report']
    counter = 0
    for item in test_list:
        if item in txt.lower():
            counter += 1
    return counter / txt.count(' ')


def test_relevence_covid(txt):
    test_words = ['corona', 'covid', '19']
    for item in test_words:
        if item in txt.lower():
            return True
    return False

if __name__ == '__main__':
    
    user = 'fmohealth'
    feeds = {'fmohealth': 'Ethiopia', 'mohzambia': 'Zambia', 'Fmohnigeria': 'Nigeria', 'MOH_Kenya': 'Kenya', 'MinofHealthUG': 'Uganda', 'MalawiGovt': 'Malawi', 'mohgovgh': 'Ghana', 'OMSMocambique': 'Mozambique', 'integrateglobal': 'Togo', 'RwandaHealth': 'Rwanda'}
    cols=['Country', 'Twitter Handle', 'Timestamp', 'Content', 'Likelyhood of Update', 'URL']
    df = pd.DataFrame(columns=cols)

    print(df)

    for twitter_handle in feeds:
        for tweet in query_tweets_from_user(twitter_handle, 40):
            translator = Translator()
            if tweet.screen_name.lower() == twitter_handle.lower():
                translated_tweet = translator.translate(tweet.text, dest='en').text
                if test_relevence_covid(translated_tweet):
                    df = df.append(pd.DataFrame([[
                        feeds[twitter_handle],
                        twitter_handle,
                        tweet.timestamp,
                        translated_tweet,
                        est_update(translated_tweet),
                        tweet.tweet_url
                    ]], columns=cols))
            
    df.to_excel(r'./output.xlsx', index=False)



    '''
    for tweet in query_tweets(user, begindate=dt.date.today() - dt.timedelta(days=1), enddate=dt.date.today()):
        if tweet.screen_name == user:
            print(tweet.text)
    '''