import datetime as dt
import pandas as pd
import yfinance as yf

msft = yf.Ticker("MSFT")

news = msft.news
df = pd.DataFrame(news)
df
