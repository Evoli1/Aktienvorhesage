import yfinance as yf, pandas as pd, numpy as np, talib as ta, matplotlib.pyplot as plt, math
from datetime import date, timedelta
from yfinance import tickers, ticker

# Analysezeitraum Heute - 729 Tage 
start = date.today() - timedelta(days=729)
end = date.today()

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
    
# Technische Indikatoren zum trainieren des Modells
# Periods sind auf Standardwerten
def indikator(asset):
    asset["RSI"] = ta.RSI(asset["Close"], timeperiod = 14)                                  # Relativer Staerke Index
    asset["ROC"] = ta.ROC(asset["Close"], timeperiod = 10)                                  # Rate Of Change
    asset["%R"] = ta.WILLR(asset["High"],asset["Low"], asset["Close"], timeperiod = 14)     # William’s Prozent Range
    asset["OBV"] = ta.OBV(asset["Close"], asset["Volume"])                                  # On-Balance-Volume
    asset["MACD"], asset["MACD_SIGNAL"], asset["MACD_HIST"] = ta.MACD(asset["Close"], fastperiod = 12, slowperiod = 26, signalperiod = 9 )      # Moving Average Convergence/Divergence
    
    # Vorhersagewerte - Wenn der Wert in 5 Tagen hoeher ist als heute dann 1 ansonsten -1
    asset["Prediction"] = np.where(asset["Close"].shift(-5) > asset["Close"], 1, -1)

# Indikatorfunktion ausfuehren
for asset in asset_list:
    indikator(asset)

# Erstelle Dataframe in dem alle Aktiendaten hintereinander gehangen werden
df = asset_list[0]
for i in range(1, len(asset_list)):
    df = df.append(asset_list[i])

# Loesche alle NaN-Werte
df.dropna(inplace=True)

# Aufteilen des Dataframes in zufaellige Train- und Test-Teilmengen
from sklearn.model_selection import train_test_split
X = df[["RSI", "ROC", "%R", "OBV", "MACD", "MACD_SIGNAL", "MACD_HIST"]]
y = df[["Prediction"]]

# Durchfuehren der zufaelligen Train- und Test-Teilmengen
# Testdatengroesse 20%, Trainingsdatengroesse 80%
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, train_size=0.8 ,random_state=0)

# Erstellen des Machine-Learning-Modells und Vorhersage aufuehren
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# n_estimators : Anzahl der Baeume im Wald | criterion : Gini-Unreinheit | random_state
# oob_score : Verwendung von Out-of-Bag-Stichproben zur Schätzung des Generalisierungswerts
model = RandomForestClassifier(n_estimators=1000, oob_score=True, criterion="gini", random_state=0)

# Clustering durchfuehren
model.fit(X_train, y_train)

# Die vorhergesagte Klasse mit der höchsten mittleren Wahrscheinlichkeitsschätzung aller Bäume
y_pred = model.predict(X_test)

# Vorhersagewahrscheinlichkeit des Modells
print("Korrekte Vorhersage in %: ", accuracy_score(y_test, y_pred, normalize=True) * 100)

# Testaktie erstellen
test_stock = yf.download(
    tickers = "NVDA", # NVDIA Aktie
    start = start,
    end = end,
    interval = "1d"
    )
# Indikator Funktion auf Testaktie anwenden
indikator(test_stock)
test_stock.dropna(inplace=True)
test_stock["Predicted"] = model.predict(test_stock[["RSI", "ROC", "%R", "OBV", "MACD", "MACD_SIGNAL", "MACD_HIST"]])

# Kauf- und Verkaufssignale
def buy_sell(asset):
    BuyPrice = []
    SellPrice = []
    flag = -1
    counter = 0
    n = 5
    
    for i in range(len(asset)):
        if asset["Predicted"][i] == 1 and counter == 0:
            if flag != 1:
                BuyPrice.append(asset["Close"][i])
                SellPrice.append(np.nan)
                flag = 1
            else:
                BuyPrice.append(np.nan)
                SellPrice.append(np.nan)
        elif asset["Predicted"][i] == -1 and counter == 0:
            if flag != 0:
                BuyPrice.append(np.nan)
                SellPrice.append(asset["Close"][i])
                flag = 0
            else:
                BuyPrice.append(np.nan)
                SellPrice.append(np.nan)
        else:
            BuyPrice.append(np.nan)
            SellPrice.append(np.nan)
        
        counter += 1
        if counter == n:
            counter = 0
            
    return(BuyPrice, SellPrice)

buysell = buy_sell(test_stock)
test_stock["Buy"] = buysell[0]
test_stock["Sell"] = buysell[1]

print(test_stock.head(10))

# Grafische Darstellung der Signale
plt.figure(figsize=(16,8))
plt.scatter(test_stock.index, test_stock["Buy"], color = "green", label = "Buy", marker = "^", alpha = 1)
plt.scatter(test_stock.index, test_stock["Sell"], color = "red", label = "Sell", marker = "v", alpha = 1)
plt.plot(test_stock.index, test_stock["Close"], alpha= 0.5)
plt.show()          

# Kalkulation eines fiktiven Eingezahlten Betrages
def calculation(asset, startUpCapital):
    capital =  [startUpCapital]
    num_stocks = 0
    
    for i in range(len(asset)):
        # Kaufe Aktie wenn Buy-Signal festgestellt wird
        if math.isnan(asset["Buy"][i]) == False:
            num_stocks = capital[i]/asset["Close"][i]   # Kaufe Aktien zum Tagespreis
            capital.append(num_stocks*asset["Close"][i])
        # Verkaufe Aktie wenn Sell-Signal festgestellt wird
        elif math.isnan(asset["Sell"][i]) == False:
            cash = num_stocks * asset["Close"][i]
            capital.append(cash)
        # Kapital bleibt gleich wenn kein Ereignis auftritt
        else:
            capital.append(capital[i])
    return capital

test_stock_capital = calculation(test_stock, 100000)

print(test_stock_capital)

# Grafische Darstellung der Kalkulation
plt.figure(figsize=(12.6, 4.6))
plt.plot(test_stock_capital)
plt.show()
