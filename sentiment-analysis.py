import pandas as pd
import re
from pandas.core.indexes.base import Index
from pandas.io.parsers import read_csv

df_twitter_data = pd.read_csv('mooietest.csv')
df_twitter_data.head(10)

df_tweetText = df_twitter_data['TweetText'].reset_index(drop=True) 
df_tweetText.head(10)

df_tweetText = df_tweetText.replace('\n','', regex=True).replace('Link:', '', regex=True)
df_tweetText = df_tweetText.replace('-->','', regex=True).replace(',', '', regex=True)
df_tweetText = df_tweetText.replace('"','', regex=True)

df_tweetText = df_tweetText.apply(lambda x: re.split('https:\/\/.*', str(x))[0])
df_tweetText = df_tweetText.apply(lambda x: re.split('http:\/\/.*', str(x))[0])
df_tweetText.head(100)

df_cleaned = df_tweetText.to_csv('cleaned.csv', index=False, encoding='utf8')

from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://uyarao:GdN29SdRDdRDKi@oege.ie.hva.nl/zuyarao')

df_tweetText.to_sql(name='zuyarao',con=engine,if_exists='replace',index=False, chunksize=1000)

# -------------------------------------------------------------------------------------------

import pandas as pd
import re


df_twitter_data = pd.read_csv('btcFile.csv')
df_twitter_data.head(10)

#drop not cleaned tweets column from dataframe
df_tweetText = df_twitter_data['TweetText'].reset_index(drop=True) 
df_tweetText = pd.DataFrame(df_tweetText)

#verwijder NaN waardes
df_tweetText = df_tweetText.dropna(subset=['TweetText'])
df_tweetText.head(10)

#cleaning of the tweets
df_tweetText = df_tweetText.replace('\n','', regex=True).replace('Link:', '', regex=True)
df_tweetText = df_tweetText.replace('-->','', regex=True).replace(',', '', regex=True)
df_tweetText = df_tweetText.replace('"','', regex=True)

# werkt op het moment niet
# df_tweetText = df_tweetText.apply(lambda x: re.split('https:\/\/.*', str(x))[0])
# df_tweetText = df_tweetText.apply(lambda x: re.split('http:\/\/.*', str(x))[0])
df_tweetText.head(10)

kaas = pd.DataFrame(df_tweetText)

df_cleaned = kaas.to_csv('btcFileCleaned.csv', index=False, encoding='utf8')

from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://uyarao:GdN29SdRDdRDKi@oege.ie.hva.nl/zuyarao')

df_tweetText.to_sql(name='btcFile',con=engine,if_exists='replace',index=False, chunksize=1000)

# --------------------------------------------------------------------------------------------


import pandas as pd
import re

#dataframes
df_tesla = pd.read_csv('mooietest.csv', index_col= 0)
df_bitcoin = pd.read_csv('btcFile.csv', index_col= 0)

#tweets csv's
tweets_tesla = pd.read_csv('cleaned.csv')
tweets_bitcoin = pd.read_csv('btcFileCleaned.csv')

#combine tesla + bitcoin dataframes
dataFrames = (df_tesla, df_bitcoin)
dataFrames_combined = pd.concat(dataFrames)
dataFrames_combined = dataFrames_combined.dropna(subset=['TweetText'])
dataFrames_combined = dataFrames_combined.reset_index(drop=True)
dataFrames_combined.head(10)

#drop TweetText column
df_drop_TweetText = dataFrames_combined.drop('TweetText', 1).drop('Unnamed: 0.1', 1).drop('Index', 1)
df_drop_TweetText.head(50)

#split Postdate into Date and Time colomn
df_drop_TweetText[['PostDates', 'PostTimes']] = df_drop_TweetText.PostDate.str.split("T", expand=True)
df_drop_TweetText = df_drop_TweetText.drop('PostDate', 1)
df_drop_TweetText['PostTimes'] = df_drop_TweetText['PostTimes'].str[:-8]

#convert like count from K to thousands
df_drop_TweetText.LikeCount = (df_drop_TweetText.LikeCount.replace(r'[K]+$', '', regex=True).astype(float) * \
     df_drop_TweetText.LikeCount.str.extract(r'[\d\.]+([K]+)', expand=False).fillna(1).replace(['K'], [10**3]).astype(int))
df_drop_TweetText.head(10)

#combine cleaned tweets tesla + bitvoin csv's
tweets_dataFrames = (tweets_tesla, tweets_bitcoin)
tweets_dataFrames_combined = pd.concat(tweets_dataFrames)
tweets_dataFrames_combined = tweets_dataFrames_combined.reset_index(drop=True)
tweets_dataFrames_combined.head(10)

#make the tweets into a df
df_total_tweets = pd.DataFrame(tweets_dataFrames_combined)
# df_total_tweets = df_total_tweets.reset_index(drop=True)
df_total_tweets.head(20)

#join cleaned tweets column to actual dataframe
cleanedTweets = tweets_dataFrames_combined['TweetText']
df_drop_TweetText = df_drop_TweetText.join(cleanedTweets)
df_drop_TweetText.index.name = 'id'
df_drop_TweetText.head()

df_cleaned = df_drop_TweetText.to_csv('cleaned_combined_df.csv', index=False, encoding='utf8')


from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://uyarao:GdN29SdRDdRDKi@oege.ie.hva.nl/zuyarao')

df_drop_TweetText.to_sql(name='cleaned_combined',con=engine,if_exists='replace',index=False, chunksize=1000)

#-----------------------------------------------------------------------------------------------------------------------------

#load in sentiment analysis dataframe
df_sentiment_analysis = pd.read_csv('Tweet_sentiment_analysis.csv')
df_sentiment_analysis.head()

#single out the analysis column
df_sentiment = df_sentiment_analysis['Analysis']
df_sentiment.index.name = 'id'
df_sentiment = pd.DataFrame(df_sentiment)
df_sentiment.head()

#change analysis to sentiment
df_sentiment.columns = ['Sentiment']
df_sentiment.head()

#add sentiment to existing dataframe

final_df = pd.merge(df_drop_TweetText, df_sentiment, on='id')

final_df.loc[final_df.Sentiment == "Negative", "Sentiment"] = 0
final_df.loc[final_df.Sentiment == "Neutral", "Sentiment"] = 1
final_df.loc[final_df.Sentiment == "Positive", "Sentiment"] = 2

final_df.head()

from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://uyarao:GdN29SdRDdRDKi@oege.ie.hva.nl/zuyarao')

final_df.to_sql(name='Sentiment',con=engine,if_exists='replace',index=False, chunksize=1000)



# tweet_about_testla = (
#     df_drop_TweetText[df_drop_TweetText['TweetText'].str.contains("Tesla", "TSLA")]
# )
# tweet_about_testla['label'] = 0

# tweet_about_bitcoin = (
#     df_drop_TweetText[df_drop_TweetText['TweetText'].str.contains("Bitcoin", "BTC")]
# )
# tweet_about_bitcoin['label'] = 1

# tweet_about_bitcoin_tesla = (
#     df_drop_TweetText[df_drop_TweetText['TweetText'].str.contains("Bitcoin", "Tesla", "TSLA", "BTC")]
# )
# tweet_about_bitcoin_tesla['label'] = 2



# tweet_about_testla = tweet_about_testla.rename(
#     {'TweetText': 'tweets'}, axis=1)
# tweet_about_bitcoin = tweet_about_bitcoin.rename(
#     {'TweetText': 'tweets'}, axis=1)
# tweet_about_bitcoin_tesla = tweet_about_bitcoin_tesla.rename(
#     {'TweetText': 'tweets'}, axis=1)


# df_all_tweets_combined = pd.concat([tweet_about_testla, tweet_about_bitcoin, tweet_about_bitcoin_tesla], axis=0)

