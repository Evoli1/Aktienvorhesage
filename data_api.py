import yfinance as yf
import pandas as pd
import numpy as np
import talib as ta
from datetime import date, timedelta

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
    asset["OBV"] = ta.OBV(asset["Close"], asset["Volume"])                                  # On -Balance Volume
    asset["MACD"], asset["MACD_SIGNAL"], asset["MACD_HIST"] = ta.MACD(asset["Close"], fastperiod = 12, slowperiod = 26, signalperiod = 9 )    # Moving Average Convergence/Divergence
    
    # Vorhersagewerte - Wenn der Wert in 5 Tagen hoeher ist als heute dann 1 ansonsten -1
    asset["Prediction"] = np.where(asset["Close"].shift(-5) > asset["Close"], 1, -1)

# Indikatorfunktion ausfuehren
for asset in asset_list:
    indikator(asset)

print(asset_list[1])
