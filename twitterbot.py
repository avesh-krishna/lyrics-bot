import tweepy
import time
from random import *
import sys
from os import environ
consumer_key = environ['CONSUMER_KEY']
consumer_secret = environ['CONSUMER_SECRET']
access_token = environ['ACCESS_KEY']
access_token_secret = environ['ACCESS_SECRET']

#%%
#api values:
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#%%
import pandas as pd
import re
df = pd.read_pickle('jbrekkie_lyrics.pkl')

#%%
def make_lyrics(df):
    stanzas = []
    for lyric in df['lyrics'].values.tolist():
        phrases = re.split("\r\n\n",lyric)
        for phrase in phrases:
            stanzas.append(phrase)
    lines = []
    for stanza in stanzas:
        lines.append(re.split("\r\n", stanza))
    return lines

def rand_lyrics(lines):
    x = len(lines)
    #print('x', x)
    start = randint(0, x-1)
    #print('start', start)
    end = randint(start+1, x)
    #print('end', end)
    return lines[start:end]

def tweetlyric(lines):
    lst = rand_lyrics(lines[randint(0,len(lines))])
    string = ''
    for line in lst:
        string = string + line + '\n'
    if len(string) > 280:
        tweetlyric(lines)
    else:
        return string

def tweet_lyric_api(lines):
    tweet_text = tweetlyric(lines)
    print(tweet_text)
    api.update_status(tweet_text)
    print("sleeping 1 hour")
    time.sleep(3480)
    tweet_lyric_api(lines)

#%%
if __name__ == "__main__":
    lines = make_lyrics(df)
    tweet_lyric_api(lines)
