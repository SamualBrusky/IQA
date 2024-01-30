import os
import json
import requests
import pandas as pd
import alpaca_trade_api as tradeapi
from statsmodels.tsa.arima.model import ARIMA
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrame
from datetime import datetime

# Alpaca API credentials
APCA_API_KEY_ID = 'PKEL9JZHFT4FKBKS70EH'
APCA_API_SECRET_KEY = 'LYV8zGzxCay9UALgD9CStIY6rFFNl3s3aTgrNwzm'
BASE_URL = 'https://paper-api.alpaca.markets'
ORDERS_URL = f'{BASE_URL}/v2/orders'
HEADERS = {'APCA-API-KEY-ID': APCA_API_KEY_ID, 'APCA-API-SECRET-KEY': APCA_API_SECRET_KEY}
rest_client = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY)

# ARIMA model
class ARIMATrader:
    def __init__(self, symbol, bars):
        self.api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, BASE_URL)
        self.symbol = symbol
        bars.index = pd.to_datetime(bars.index, utc=True)  # Ensure the index is in datetime format
        bars = bars.tz_localize(None)  # Remove timezone information
        bars = bars.sort_index()  # Sort the DataFrame by the index
        self.df = bars.dropna()  # Remove rows with missing data
        self.df = self.df.asfreq('T')  # Ensure minute frequency
        self.model = ARIMA(self.df.close, order=(5, 1, 5))  # Adjust order parameters as needed
        self.model_fit = self.model.fit(method_kwargs={'maxiter': 10000})
        self.predictions = []

    def predict(self):
        try:
            forecast = self.model_fit.forecast(steps=1).iloc[0]
            next_timestamp = self.df.index[-1] + pd.DateOffset(1)
            forecast_series = pd.Series(forecast, index=[next_timestamp])
            return forecast_series
        except Exception as e:
            print(f"Error in predicting: {e}")
            return None

    def trade(self):
        current_price = self.api.get_latest_trade(self.symbol).price
        prediction = self.predict()
        tick_size = 0.01
        base_price = current_price

        take_profit_price_Buy = max(base_price + 1, round(current_price * 1.001, 1))  # Round to five decimal places (cents)
        stop_loss_price_Buy = max(base_price - 1, round(current_price * 0.999, 1))  # Round to five decimal places (cents)
        take_profit_price_Short = max(base_price + 1, round(current_price * 0.999, 1))  # Round to five decimal places (cents)
        stop_loss_price_Short = max(base_price - 1, round(current_price * 1.001, 1))  # Round to five decimal places (cents)

        if take_profit_price_Buy <= stop_loss_price_Buy:
            take_profit_price_Buy = stop_loss_price_Buy + 0.01

        if take_profit_price_Short >= stop_loss_price_Short:
            take_profit_price_Short = stop_loss_price_Short - 0.01

        if prediction is not None:
            if prediction.iloc[0] > current_price:
                print(f"Current Price: {current_price}")
                print(f"Predicted Price: {prediction.iloc[0]}")
                print(f"Take Profit Price: {take_profit_price_Buy}")
                print(f"Stop Loss Price: {stop_loss_price_Buy}")
                order_response = self.api.submit_order(
                    symbol=self.symbol,
                    qty=200,
                    side='buy',  # Buy the stock
                    type='limit',
                    time_in_force='gtc',
                    limit_price=current_price,
                    order_class='bracket',
                    take_profit={
                        "limit_price": take_profit_price_Buy
                    },
                    stop_loss={
                        "stop_price": stop_loss_price_Buy,
                        "limit_price": stop_loss_price_Buy  # Sell at market if the price drops below stop-loss
                    }
                )
            else:
                print(f"Current Price: {current_price}")
                print(f"Predicted Price: {prediction.iloc[0]}")
                print(f"Take Profit Price: {take_profit_price_Short}")
                print(f"Stop Loss Price: {stop_loss_price_Short}")
                order_response = self.api.submit_order(
                    symbol=self.symbol,
                    qty=200,
                    side='sell',  # Sell the stock
                    type='limit',
                    time_in_force='gtc',
                    limit_price=current_price,
                    order_class='bracket',
                    take_profit={
                        "limit_price": take_profit_price_Short
                    },
                    stop_loss={
                        "stop_price": stop_loss_price_Short,
                        "limit price": stop_loss_price_Short   # Sell at market if the price drops below stop-loss
                    }
                )

    def place_order(self, qty, side, type, time_in_force, order_class):
        data = {
            'symbol': self.symbol,
            'qty': qty,
            'side': side,
            'type': type,
            'time_in_force': time_in_force,
            'order_class': order_class
        }

        r = requests.post(ORDERS_URL, json=data, headers=HEADERS)
        return json.loads(r.content)

if __name__ == '__main__':
    symbol = 'SPY'
    bars = rest_client.get_bars(symbol, TimeFrame.Minute, '2024-01-01', '2024-01-29').df
    trader = ARIMATrader(symbol=symbol, bars=bars)
    trader.trade()
