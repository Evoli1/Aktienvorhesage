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

for ticker in tickers:
    url = finviz_url + ticker
    
    req = Request(url=url, headers={'user-agent': 'my-app'})
    response = urlopen(req)

    html = BeautifulSoup(response, features='html.parser')
    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table
    
#Erstellen Dataframe für Analyse 
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

#Calculating Sentiment Scores
vader = SentimentIntensityAnalyzer()
#Anzeigen Ergebnisse von compound-Punkte in Tabelle
df['compound'] = ''
df['negative'] = ''
df['neutral'] = ''
df['positive'] = ''

df['compound'] = df['title'].apply(lambda x: vader.polarity_scores(x)['compound'])
df['negative'] = df['title'].apply(lambda x: vader.polarity_scores(x)['neg'])
df['neutral'] = df['title'].apply(lambda x: vader.polarity_scores(x)['neu'])
df['positive'] = df['title'].apply(lambda x: vader.polarity_scores(x)['pos'])

#Grafische Darstellung der Analyse 
df['Date'] = pd.to_datetime(df.date).dt.date
plt.figure(figsize=(10,8))
mean_df = df.groupby(['ticker','Date']).mean().unstack()
mean_df = mean_df.xs('compound', axis="columns").transpose()
mean_df.plot(kind="bar")
plt.show()

##Vorhersagemodell aufbauen, z.B für APPL
parsed_text = []
ticker = "APPL"
for row in news_table.findAll('tr'):

        title = row.a.text
        date_data = row.td.text.split(' ')

        if len(date_data) == 1:
            time = date_data[0]
        else:
            date = date_data[0]
            time = date_data[1]

        parsed_text.append([ticker, date, time, title])

df_ml = pd.DataFrame(parsed_text, columns=['ticker', 'date', 'time', 'title'])

#Re-Formatierung der Zeitdaten fürs Kombinieren zwei Datensätzen
import locale
from datetime import datetime
locale.setlocale(locale.LC_TIME, locale.normalize("en"))
df_ml['date']=pd.to_datetime(df_ml['date'], format='%b-%d-%y')

#Calculating Sentiment Scores
vader = SentimentIntensityAnalyzer()
df_ml['compound'] = ''
df_ml['negative'] = ''
df_ml['neutral'] = ''
df_ml['positive'] = ''
df_ml['compound'] = df_ml['title'].apply(lambda x: vader.polarity_scores(x)['compound'])
df_ml['negative'] = df_ml['title'].apply(lambda x: vader.polarity_scores(x)['neg'])
df_ml['neutral'] = df_ml['title'].apply(lambda x: vader.polarity_scores(x)['neu'])
df_ml['positive'] = df_ml['title'].apply(lambda x: vader.polarity_scores(x)['pos'])

#Durchschnittliche compound-Punkte jedes Tages 
df_ml = df_ml[['date','compound']]
df_ml = df_ml.groupby(['date'])
ml_average = df_ml.sum()/df_ml.count()

#Aktienkursendaten
from datetime import date, timedelta
import yfinance as yf
from yfinance import tickers, ticker

start = date.today() - timedelta(days=365)
end = date.today()
datalist = yf.download('FB', 
                      start= start, 
                      end= end, 
                      progress=False,
)
datalist[['Close']]
df_data = pd.DataFrame(datalist)
df_data = df_data.sort_index(ascending=False, axis=0)

#Kombinieren zwei Datensätzen
combi = pd.concat([ml_average, df_data], axis=1)
combi = combi.sort_index(ascending=False, axis=0)
#Bearbeitung des kombinierten Datensatzes
combi = combi[['Close','compound']]
combi.dropna(inplace=True)

#Einstellung Variablen und Zielwert
x = combi.iloc[:, 0:1].values 
y = combi.iloc[:, 1].values 
# Anpassen der Random-Forest-Regression an den Datensatz
from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor(n_estimators = 100, random_state = 0)
regressor.fit(x, y)  
Y_pred = regressor.predict(np.array([6.5]).reshape(1, 1)) #Output-testen bei der Wertenänderung

# Visualisierung der Ergebnisse der Random Forest Regression


# Erstellen eines Wertebereichs vom Mindestwert von x bis zum Höchstwert von x mit einer Differenz von 0,01 zwischen zwei aufeinanderfolgenden Werten
X_grid = np.arange(min(x), max(x), 0.01)

X_grid = X_grid.reshape((len(X_grid), 1))

# Streudiagramm für Originaldaten
plt.scatter(x, y, color = 'blue')

# Darstellung die prognostizierte Daten grafisch
plt.plot(X_grid, regressor.predict(X_grid),
        color = 'green')
plt.title('Random Forest Regression')
plt.xlabel('Close')
plt.ylabel('Sentiment')
plt.show()
