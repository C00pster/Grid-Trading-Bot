from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
import pandas as pd
from datetime import datetime, timedelta

def update_btc_bars():
    df = pd.read_csv("btc_bars.csv", parse_dates=["ds"])
    current_date = datetime.now()
    df = df[df["ds"] > current_date - timedelta(days=365)]
    df.to_csv("btc_bars.csv", index=False)

    df = pd.read_csv("btc_bars.csv")
    last_timestamp = df.iloc[-1]["ds"]
    start_time = datetime.strptime(last_timestamp, "%Y-%m-%d %H:%M:%S")
    start_time += timedelta(minutes=1)

    client = CryptoHistoricalDataClient()
    request_params = CryptoBarsRequest(
                            symbol_or_symbols=["BTC/USD"],
                            timeframe=TimeFrame.Minute,
                            start=start_time,
                            end=datetime.now(),
                            )

    btc_bars = client.get_crypto_bars(request_params)

    btc_bars_df = btc_bars.df.reset_index()
    btc_bars_df = btc_bars_df[["timestamp", "close"]]
    btc_bars_df["timestamp"] = btc_bars_df["timestamp"].dt.tz_localize(None)
    btc_bars_df.rename(columns={"timestamp": "ds", "close": "y"}, inplace=True)

    df = pd.concat([df, btc_bars_df])
    df.to_csv("btc_bars.csv", index=False)