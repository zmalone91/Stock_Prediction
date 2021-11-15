# Standard Library Imports
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt 
# import seaborn as sns

# # Project Specific Library Imports
# import streamlit as st
# from datetime import date
# import yfinance as yf
# from fbprophet import Prophet
# from fbprophet.plot import plot_plotly
# from plotly import graph_objs as go

import streamlit as st
from forecast import show_forecast_page
from sentiment import show_sentiment_page

st.set_page_config(layout='wide')

analysis = st.selectbox('Choose Financial Analysis or Sentiment Analysis', ('Financial Report', 'Sentiment Report'),index=0)

if analysis == 'Financial Report':
    show_forecast_page()
else:
    show_sentiment_page()

st.sidebar.title('Project Overview')
st.sidebar.text('Click X to Hide')
st.sidebar.subheader('What The Models Can Be Used For')
st.sidebar.subheader('Financial Report')
st.sidebar.write('Historical stock price data from 2015 to present for the top 100 NASDAQ stocks by Market Cap can be analyzed in both a line graph and candlsetick for YTD to visualize trading history and recent overall trend. Using Facebook`s powerful fbprophet library we perform a simple Time Series Forecast on the data for a specified Years of Prediction.')
st.sidebar.write('')
st.sidebar.subheader('Sentiment Report')
st.sidebar.write('Using Tweepy, we analyze the sentiment of the most recent tweets for whatever stock ticker we have selected. We look at the overall Positive/Neutral/Negative analysis of the tweets as well as some information about the users who posted them with the help of the Twitter API. Additionally, we can create WordClouds, visualizations, and even breakout into different types of Machine Learning tasks from the data we collect from the tweets and users.')
st.sidebar.write('')
st.sidebar.subheader('References')
st.sidebar.write('fbprophet documentation')
st.sidebar.write('https://pypi.org/project/fbprophet/')
st.sidebar.write('Tweepy documentation')
st.sidebar.write('https://docs.tweepy.org/en/latest/')

