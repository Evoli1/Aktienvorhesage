import yfinance as yf

# Tricker Objekt fuer Microsoft Cooperation "MSFT" Aktie
msft = yf.Ticker("MSFT")

# Historische Daten aus der Datenbank herrunterladen
hist = msft.history(period="5y", interval="1d" )

print(hist)