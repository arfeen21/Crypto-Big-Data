from nltk.probability import HeldoutProbDist
from pandas.io.parsers import read_csv
from sklearn.utils.validation import check_non_negative
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re 
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

df = pd.read_csv('cleaned_combined_df.csv')
df.head()

tweetText_df = df.drop('User', 1).drop('Handle', 1).drop('LikeCount', 1).drop('Crypto', 1).drop('PostDates', 1).drop('PostTimes', 1)
tweetText_df.head()

def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

def getPolarity(text):
    return TextBlob(text).sentiment.polarity

tweetText_df['Subjectivity'] = tweetText_df['TweetText'].apply(getSubjectivity)
tweetText_df['Polarity'] = tweetText_df['TweetText'].apply(getPolarity)

tweetText_df.head(50)

#create function to compute positive, neutral and negative analysis

def getAnalysis(score):
    if score < 0:
         return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'

tweetText_df['Analysis'] = tweetText_df['Polarity'].apply(getAnalysis)
tweetText_df.head(50)



# percentage negative tweets
ntweets = tweetText_df[tweetText_df.Analysis == 'Negative']
ntweets = ntweets['TweetText']
ntweets

round( (ntweets.shape[0] / df.shape[0]) * 100, 1)

# percentage positive tweets
ptweets = tweetText_df[tweetText_df.Analysis == 'Positive']
ptweets = ptweets['TweetText']
ptweets

round( (ptweets.shape[0] / df.shape[0]) * 100 , 1)

# percentage neutral tweets
ptweets = tweetText_df[tweetText_df.Analysis == 'Neutral']
ptweets = ptweets['TweetText']
ptweets

round( (ptweets.shape[0] / df.shape[0]) * 100 , 1)

# Plotting and visualizing the counts
plt.title('Sentiment Analysis')
plt.xlabel('Sentiment')
plt.ylabel('Counts')
tweetText_df['Analysis'].value_counts().plot(kind = 'bar')
plt.show()


tweetText_df['Analysis'].value_counts()

# make a csv file of sentiment analysis
tweetText_df = tweetText_df.to_csv('Tweet_sentiment_analysis.csv', index=False, encoding='utf8')