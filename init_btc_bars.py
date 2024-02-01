from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta

client = CryptoHistoricalDataClient()

request_params = CryptoBarsRequest(
                        symbol_or_symbols=["BTC/USD"],
                        timeframe=TimeFrame.Minute,
                        start=datetime.now() - timedelta(days=365),
                        end=datetime.now(),
                        )

btc_bars = client.get_crypto_bars(request_params)

btc_bars_df = btc_bars.df.reset_index()

btc_bars_df = btc_bars_df[["timestamp", "close"]]
btc_bars_df["timestamp"] = btc_bars_df["timestamp"].dt.tz_localize(None)
btc_bars_df.rename(columns={"timestamp": "ds", "close": "y"}, inplace=True)

btc_bars_df.to_csv("btc_bars.csv", index=False)