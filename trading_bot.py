from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime

# client = CryptoHistoricalDataClient()

# request_params = CryptoBarsRequest(
#                         symbol_or_symbols=["BTC/USD"],
#                         timeframe=TimeFrame.Minute,
#                         start=datetime.strptime("2020-01-01", "%Y-%m-%d"),
#                         end=datetime.strptime("2023-12-17", "%Y-%m-%d"),
#                         )

# btc_bars = client.get_crypto_bars(request_params)

# btc_bars.df.to_csv("btc_bars.csv")

import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import pickle

df = pd.read_csv("btc_bars.csv")

m = Prophet()
m.fit(df)

with open("model.pkl", "rb") as f:
    m = pickle.load(f)

future = m.make_future_dataframe(periods=1)
future.tail()

forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

fig1 = m.plot(forecast)
plt.show()

# with open('model.pkl', 'wb') as f:
#     pickle.dump(m, f)