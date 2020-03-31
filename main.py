from __future__ import print_function
from twitterscraper import query_tweets_from_user
import datetime as dt
import json
import pandas as pd
from googletrans import Translator

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SAMPLE_SPREADSHEET_ID = '1410KYTh48ju_aahMhDe2-BmozY3ixIopn2z7vkq9tGs'
SAMPLE_RANGE_NAME = 'Sheet1!B2:G23'
values = []


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

    # handle google sheets api authentication
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    service = build('sheets', 'v4', credentials=creds)

    

    feeds = {'fmohealth': 'Ethiopia', 'mohzambia': 'Zambia', 'Fmohnigeria': 'Nigeria', 'MOH_Kenya': 'Kenya', 'MinofHealthUG': 'Uganda', 'MalawiGovt': 'Malawi', 'mohgovgh': 'Ghana', 'OMSMocambique': 'Mozambique', 'integrateglobal': 'Togo', 'RwandaHealth': 'Rwanda'}
    cols=['Country', 'Twitter Handle', 'Timestamp', 'Content', 'Likelyhood of Update', 'URL']
    df = pd.DataFrame(columns=cols)

    # Pull tweets
    for twitter_handle in feeds:
        for tweet in query_tweets_from_user(twitter_handle, 10):
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
                        'https://twitter.com%s' % tweet.tweet_url
                    ]], columns=cols))
            
    values = df.sort_values(by='Timestamp', ascending=False).head(20).values.tolist()

    # Prepare 
    for i in range(len(values)):
        for j in range(len(values[i])):
            values[i][j] = str(values[i][j])
    body = {
    'values': values
    }

    sheet = service.spreadsheets()
    result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME,
                                valueInputOption='RAW', 
                                body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))
