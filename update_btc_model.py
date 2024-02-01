import pandas as pd
import pickle
from prophet import Prophet
import matplotlib.pyplot as plt
from update_bars import update_btc_bars

while True:
    update_btc_bars()

    df = pd.read_csv("btc_bars.csv")

    m = Prophet()
    m.fit(df)

    future = m.make_future_dataframe(periods=1)
    future.tail()

    forecast = m.predict(future)
    forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
    forecast.set_index("ds", inplace=True)

    with open("forecast.pkl", "wb") as f:
        pickle.dump(forecast, f)