# Import libraries needed for your script functionality
import os
import json
import requests
import pandas as pd
import alpaca_trade_api as tradeapi
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt
from alpaca_trade_api import REST, TimeFrame
def ARIMATrade_Web():

# Alpaca API credentials
    APCA_API_KEY_ID = 'PKK6ELKSXUJBT67ECJAT'
    APCA_API_SECRET_KEY = '0NEItQlaS4g59lEyfOpQVsJvog5PGkfCCVu0AlnM'
    BASE_URL = 'https://paper-api.alpaca.markets'
    ORDERS_URL = f'{BASE_URL}/v2/orders'
    HEADERS = {'APCA-API-KEY-ID': APCA_API_KEY_ID, 'APCA-API-SECRET-KEY': APCA_API_SECRET_KEY}
    rest_client = REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY)
    class ARIMATrader:
        def __init__(self, symbol, bars):
            self.api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, BASE_URL)
            self.symbol = symbol
            self.df = pd.read_csv(bars, index_col='Date', parse_dates=True)
            self.df = self.df.asfreq('m')
            self.model = ARIMA(self.df.Close, order=(10, 1, 10))
            self.model_fit = self.model.fit(method_kwargs={'maxiter':10000})
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

            take_profit_price = max(base_price + 1, round(current_price * 1.001, -1))  # Round to five decimal places (cents)
            stop_loss_price = max(base_price - 1, round(current_price * 0.999, 1))  # Round to five decimal places (cents)
  
            if take_profit_price <= stop_loss_price:
                take_profit_price = stop_loss_price + 0.01


            if prediction is not None:
                if prediction.iloc[0] > current_price:
                    print(f"Current Price: {current_price}")
                    print(f"Predicted Price: {prediction.iloc[0]}")
                    print(f"Take Profit Price: {take_profit_price}")
                    print(f"Stop Loss Price: {stop_loss_price}")
                    order_response = self.api.submit_order(
                    symbol=self.symbol,
                    qty=200,
                    side='buy',  # Buy the stock
                    type='limit',
                    time_in_force='gtc',
                    limit_price=current_price,
                    order_class='bracket',
                    take_profit={
                    "limit_price": take_profit_price
                    },
                    stop_loss={
                    "stop_price": stop_loss_price,
                    "limit_price": stop_loss_price  # Sell at market if the price drops below stop-loss
                    }
                    )
                else :
                    print(f"Current Price: {current_price}")
                    print(f"Predicted Price: {prediction.iloc[0]}")
                    print(f"Take Profit Price: {take_profit_price}")
                    print(f"Stop Loss Price: {stop_loss_price}")
                    order_response = self.api.submit_order(
                    symbol=self.symbol,
                    qty=200,
                    side='sell',  # Buy the stock
                    type='limit',
                    time_in_force='gtc',
                    limit_price=current_price,
                    order_class='bracket',
                    take_profit={
                    "limit_price": take_profit_price
                    },
                    stop_loss={
                    "stop_price": stop_loss_price,
                    "limit_price": stop_loss_price  # Sell at market if the price drops below stop-loss
                    }
                    )
        def place_order(self, qty, side, type, time_in_force, order_class):
            data = {
            'symbol': self.symbol,
            'qty': qty,
            'side': side,
            'type': type,
            'time_in_force': time_in_force,
            'order_class' : order_class
            }

            r = requests.post(ORDERS_URL, json=data, headers=HEADERS)
            return json.loads(r.content)

    if __name__ == '__main__':
        ARIMATrade_Web()
        trader = ARIMATrader(symbol='SPY', bars = rest_client.get_bars("SPY", TimeFrame.Minute, "2023-9-01", "2023-09-02").df)

        trader.trade()
