import yfinance as yf

df = yf.download("^DJI", period="max", interval="1d")
print(df.head())
print(df.index)
