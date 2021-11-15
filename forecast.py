#Standard Library Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns

# Project Specific Library Imports
import streamlit as st
from datetime import date
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go
start = '2015-01-01'
end = date.today().strftime("%Y-%m-%d")

def show_forecast_page():
    st.title("NASDAQ Stock Analysis and Time Series Forecast")

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

    n_years = st.slider('Years of Prediction:', 1, 4)
    period = n_years * 365

    @st.cache
    def load_data(ticker):
        data = yf.download(ticker, start, end)
        data.reset_index(inplace=True)
        return data

    data = load_data(selected_stock)

    st.subheader('Raw Data')

    show_full_data = st.checkbox('Show Full Historical Data',value=False)

    if show_full_data:
        st.write(data.iloc[::-1])
    else:
        st.write(data.iloc[::-1].head())

    col1, col2 = st.columns(2)

    def plot_raw_data():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='Open'))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Close'))
        fig.layout.update(title_text='Time Series Data', xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)

    with col1:
        plot_raw_data()

    def plot_candles():
        df = data[data['Date']>='2021-01-01']
        fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                        open=df['Open'],
                        high=df['High'],
                        low=df['Low'],
                        close=df['Close'])])
        fig.layout.update(title_text='Year to Date Candlestick')
        st.plotly_chart(fig)

    with col2:
        plot_candles()

    # Forecasting
    df_train = data[['Date', 'Close']]
    df_train = df_train.rename(columns={'Date':'ds', 'Close':'y'})

    m = Prophet()

    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)

    st.subheader('Forecast Data')

    show_forecast_data = st.checkbox('Show Full Forecast Data',value=False)

    if show_forecast_data:
        st.write(forecast.iloc[::-1])
    else:
        st.write(forecast.iloc[::-1].head())

    # st.write(forecast.tail())

    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1)

    st.write('Forecast Components')
    fig2 = m.plot_components(forecast)
    st.write(fig2)