import time
import datetime
import pandas as pd
import pickle
import os
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import LimitOrderRequest
from alpaca.trading.enums import OrderSide, OrderType, TimeInForce

load_dotenv()

alpaca_public_key = os.getenv("ALPACA_PUBLIC_KEY")
alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")

trading_client = TradingClient(alpaca_public_key, alpaca_secret_key, paper=True)

def get_available_qty(symbol_str):
    positions = trading_client.get_open_position(symbol_or_asset_id=symbol_str)
    return positions.qty_available

def get_usd_available():
    account = trading_client.get_account()
    return account.cash

def update_grid(projected_market_price, upper_bound=None, lower_bound=None):
    trading_client.cancel_orders() # Clears prior grid
    btc_available = get_available_qty("BTCUSD")
    usd_available = get_usd_available()
    grid_strategy = pd.read_csv("grid_strategy.csv")
    for index, (factor, percent_sell, percent_buy) in grid_strategy.iterrows():
        limit_price = float(projected_market_price) * float(factor)
        if percent_sell != 0:
            sell_qty = float(btc_available) * float(percent_sell)
            if sell_qty * float(limit_price) < 1: continue
            limit_order_request = LimitOrderRequest(
                symbol="BTCUSD",
                qty=sell_qty,
                side=OrderSide.SELL,
                type=OrderType.LIMIT,
                time_in_force=TimeInForce.GTC,
                limit_price=limit_price,
            )
            trading_client.submit_order(limit_order_request)
            print("Sell order submitted for {} BTC at ${}".format(sell_qty, limit_price))
        elif percent_buy != 0:
            buy_qty = (float(usd_available) * float(percent_buy)) / float(limit_price)
            if buy_qty * float(limit_price) < 1: continue
            limit_order_request = LimitOrderRequest(
                symbol="BTCUSD",
                qty=buy_qty,
                side=OrderSide.BUY,
                type=OrderType.LIMIT,
                time_in_force=TimeInForce.GTC,
                limit_price=limit_price,
            )
            trading_client.submit_order(limit_order_request)
            print("Buy order submitted for {} BTC at ${}".format(buy_qty, limit_price))
        

while True:
    start_time = datetime.datetime.now()
    minute = start_time.minute
    with open("forecast.pkl", "rb") as f:
        forecast = pickle.load(f)
    projected_market = forecast.asof(start_time)[["yhat", "yhat_lower", "yhat_upper"]]
    update_grid(projected_market["yhat"], projected_market["yhat_upper"], projected_market["yhat_lower"])
    time.sleep(240)

    while True:
        current_time = datetime.datetime.now()
        if current_time.minute != (minute + 4) % 60:
            break
        time.sleep(1)
