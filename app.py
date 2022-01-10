import streamlit as st
import yfinance as yf, pandas as pd, numpy as np, talib as ta, matplotlib.pyplot as plt, math
from datetime import date, timedelta
from yfinance import tickers, ticker

st.title('Aktienvorhersage App')

stocks = ('FB', 'AMZN', 'AAPL', 'NFLX', 'GOOG')
selected_stock = st.selectbox('Wählen Sie eine Aktien', stocks)

n_months = st.slider('Analysezeitraum (Monat):', 1, 24)
period = n_months * 30

# Analysezeitraum Heute - 729 Tage 
start = date.today() - timedelta(days=period)
end = date.today()

@st.cache
def load_data(ticker):
    data = yf.download(ticker, start, end)
    data.reset_index(inplace=True)
    return data

data = load_data(selected_stock)

st.subheader('Raw data')
st.write(data)

# Download der FANG Aktiendaten
assets = ["FB", "AMZN", "AAPL", "NFLX", "GOOG"]
asset_list = list()     # Liste der Dataframes
for asset in assets:
    asset = yf.download(
        tickers = asset,
        start = start,
        end = end,
        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval = "1d"
        )
    asset_list.append(asset)


from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('vader_lexicon')

#Download 100 aktuell Header von jeder Aktie
finviz_url = 'https://finviz.com/quote.ashx?t='
tickers = ['FB','AMZN','AAPL','NFLX','GOOG']

news_tables = {}

def load_news(ticker):
    url = finviz_url + ticker
    
    req = Request(url=url, headers={'user-agent': 'my-app'})
    response = urlopen(req)

    html = BeautifulSoup(response, features='html.parser')
    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table
    parsed_data = []
    for ticker, news_table in news_tables.items():

        for row in news_table.findAll('tr'):

            title = row.a.text
            date_data = row.td.text.split(' ')

            if len(date_data) == 1:
                time = date_data[0]
            else:
                date = date_data[0]
                time = date_data[1]

            parsed_data.append([ticker, date, time, title])

    df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'title'])
    return df

news = load_news(selected_stock)
st.subheader('100 aktuelle Headline News')
st.write(news)
    
#Calculating Sentiment Scores
vader = SentimentIntensityAnalyzer()
#Anzeigen Ergebnisse von compound-Punkte in Tabelle
news['compound'] = ''
news['negative'] = ''
news['neutral'] = ''
news['positive'] = ''

news['compound'] = news['title'].apply(lambda x: vader.polarity_scores(x)['compound'])
news['negative'] = news['title'].apply(lambda x: vader.polarity_scores(x)['neg'])
news['neutral'] = news['title'].apply(lambda x: vader.polarity_scores(x)['neu'])
news['positive'] = news['title'].apply(lambda x: vader.polarity_scores(x)['pos'])    

#Grafische Darstellung der Analyse 
news['Date'] = pd.to_datetime(news.date).dt.date
plt.figure(figsize=(10,8))
mean_df = news.groupby(['ticker','Date']).mean().unstack()
mean_df = mean_df.xs('compound', axis="columns").transpose()
mean_df.plot(kind="bar")
graph1 = plt.show()

st.subheader('Sentiment Analyse - compound-Punkt')
st.set_option('deprecation.showPyplotGlobalUse', False) #disable warning
st.pyplot(graph1)
