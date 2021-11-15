import pandas as pd
import numpy as np
import regex as re
import streamlit as st
from datetime import datetime, date
from plotly import graph_objs as go
from textblob import TextBlob
from wordcloud import WordCloud

# Import Twitter API Sentiment Analysis components
import tweepy
from tweepy import Stream
from textblob import TextBlob
from wordcloud import WordCloud
# Save API keys in twitter_keys.py
from twitter_keys import consumer_key, consumer_secret, access_token, access_token_secret
# Create authentication object using OAuth 2
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Set the access token and access token secret
auth.set_access_token(access_token, access_token_secret)
# Create API object and pass in auth information
api = tweepy.API(auth, wait_on_rate_limit=True)

def show_sentiment_page():
	# Collect Twitter Data
    st.title('Twitter Sentiment Analysis')

    # Top 100 NASDAQ stocks in terms of Market Cap
    # csv available here at https://www.nasdaq.com/market-activity/stocks/screener
    stocks = ('AAPL','MSFT','GOOG','GOOGL','AMZN','TSLA','FB','NVDA','TSM','JPM',
                'V','BABA','JNJ','UNH','WMT','BAC','ADI','HD','MA','PG','ASML','ADBE',
                'NFLX','CRM','NTES','DIS','PFE','XOM','NKE','NVO','ORCL','TM','TMO',
                'LLY','PYPL','KO','CMCSA','CSCO','ACN','AVGO','COST','ABT','PEP','CVX',
                'DHR','VZ','MRK','SHOP','ABBV','INTC','WFC','SE','MCD','UPS','QCOM',
                'NVS','AZN','MS','AMD','T','INTU','TXN','LIN','NEE','SAP','LOW','ANET',
                'MDT','UNP','SCHW','HON','SONY','RY','TMUS','BLK','PM','AMAT','CHTR',
                'AXP','BHP','NOW','C','GS','TD','UL','BBL','JD','RTX','HDB','BMY',
                'SBUX','TTE','BA','SNY','TGT','ISRG','EL','CVS','AMT','ABNB')


    selected_stock = st.selectbox('Select Stock Ticker', stocks)

    st.write('')

    num_tweets = st.selectbox('Number of Tweets to Analyze (Demo Warning: 500+ can be slow and may raise rate limit issues with free Twitter API.', (100, 250, 500, 1000))

    search_words = ['$' + selected_stock]

    tweets = api.search_tweets(q=search_words, count=num_tweets)

    df = pd.DataFrame( [(tweet.id, tweet.text, api.get_status(tweet.id).created_at, tweet.user.screen_name, tweet.user.followers_count, tweet.user.friends_count, tweet.user.verified) for tweet in tweets], columns=['Tweet ID', 'Tweet', 'Created', 'Screen_Name', 'Followers', 'Following', 'Verified'] )

	# Create a function to identify the day of the week
    def weekDay(created):
	    i = created.weekday()
	    if i == 0:
	        return 'Sunday'
	    elif i == 1:
	        return 'Monday'
	    elif i == 2:
	        return 'Tuesday'
	    elif i == 3:
	        return 'Wednesday'
	    elif i == 4:
	        return 'Thursday'
	    elif i == 5:
	        return 'Friday'
	    else:
	        return 'Saturday' 

    df['Day'] = df['Created'].apply(weekDay)

	# Clean text using RegEx

    def cleanText(text):
	    text = re.sub(r'@[A-Za-z0-9_]+', '', text)
	    text = re.sub(r'#', '', text)
	    text = re.sub(r'RT[\s]+', '', text)
	    text = re.sub(r'https?:\/\/\S+', '', text)
	    text = re.sub(r':', '', text)
	    
	    return text

    df['Tweet'] = df['Tweet'].apply(cleanText)

	# Create a function to bring in the subjectivity

    def getSubjectivity(text):
	    return TextBlob(text).sentiment.subjectivity

    def getPolarity(text):
	    return TextBlob(text).sentiment.polarity

	# Create two new columns, Subjectivity and Polarity

    df['Subjectivity'] = df['Tweet'].apply(getSubjectivity)

    df['Polarity'] = df['Tweet'].apply(getPolarity)


	# Create a function to determine positive, negative, and neutral analysis

    def getAnalysis(score):
	    if score < 0:
	        return 'Negative'
	    elif score == 0:
	        return 'Neutral'
	    else:
	        return 'Positive'

    df['Analysis'] = df['Polarity'].apply(getAnalysis)

    df = df[['Analysis','Tweet','Screen_Name', 'Followers']].sort_values(by=['Followers'],ascending=False)

    st.write('')
    st.write('')

	# Create final df before table creation function
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Tweets')
        st.write(df)

    all_words = ' '.join( [tweets for tweets in df['Tweet']] )
    wc = WordCloud(width = 500, height = 300, random_state = 21, max_font_size = 119).generate(all_words)
    #fig = go.Figure()
    with col2:
        st.subheader('Word Cloud')
        st.image(wc.to_array())

    st.write('')
    st.write('')

    pos_tweets = len(df[df['Analysis']=='Positive']) / len(df['Analysis'])
    neut_tweets = len(df[df['Analysis']=='Neutral']) / len(df['Analysis'])
    neg_tweets = len(df[df['Analysis']=='Negative']) / len(df['Analysis'])

    st.write(f'Positive Tweets: {pos_tweets:.0%}')
    st.write(f'Neutral Tweets: {neut_tweets:.0%}')
    st.write(f'Negative Tweets: {neg_tweets:.0%}')
    
    st.bar_chart(df['Analysis'].value_counts(), )

