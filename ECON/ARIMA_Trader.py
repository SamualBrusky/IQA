import os
import json
import requests
import pandas as pd
import alpaca_trade_api as tradeapi
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt

# Alpaca API credentials
APCA_API_KEY_ID = 'PKI455172NM1B6J20DVW'
APCA_API_SECRET_KEY = 'yrWtomrUTLbRLBOlnKHJU5gdGh9WxaVyiJab9cCvS'
BASE_URL = 'https://paper-api.alpaca.markets'
ORDERS_URL = f'{BASE_URL}/v2/orders'
HEADERS = {'APCA-API-KEY-ID': APCA_API_KEY_ID, 'APCA-API-SECRET-KEY': APCA_API_SECRET_KEY}

# ARIMA model
class ARIMATrader:
    def __init__(self, symbol, path_to_data):
        self.api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, BASE_URL)
        self.symbol = symbol
       # v1
       # self.df = pd.read_csv(path_to_data, index_col=0, parse_dates=True)
       # v2
       # self.df = pd.read_csv(path_to_data, index_col='Date', parse_dates=True)
        self.df = pd.read_csv(path_to_data, index_col='Date', parse_dates=True)
        self.df = self.df.asfreq('D')  # Assuming daily frequency, adjust as needed
        self.model = ARIMA(self.df.Close, order=(5, 1, 0))
        self.model_fit = self.model.fit()
        self.predictions = []

#Predict v1
    #def predict(self):
        #forecast, stderr, conf_int = self.model_fit.forecast(steps=1)
        #return forecast[0]
    #    try:
    #        forecast = self.model_fit.forecast(steps=1)[0]
    #        return forecast
    #    except Exception as e:
    #        print(f"Error in predicting: {e}")
    #        return None
#Predict v2   
    #def predict(self):
    #    try:
    #        forecast = self.model_fit.forecast(steps=1)[0]
    #        return forecast
    #    except Exception as e:
    #        print(f"Error in predicting: {e}")
    #        return None
    
    def predict(self):
        try:
            forecast = self.model_fit.forecast(steps=1)[0]
            next_timestamp = self.df.index[-1] + pd.DateOffset(1)  # Assuming daily frequency, adjust as needed
            forecast_series = pd.Series(forecast, index=[next_timestamp])
            return forecast_series
        except Exception as e:
            print(f"Error in predicting: {e}")
            return None

    def trade(self):
        current_price = self.api.get_latest_trade(self.symbol).price
        prediction = self.predict()
        tick_size = 0.01  # Example: $0.01 tick size

        take_profit_price = round(current_price * 1.001, 2)  # Round to two decimal places (cents)
        stop_loss_price = round(current_price * 0.999, 2)  # Round to two decimal places (cents)

        if prediction is not None:
            if prediction.iloc[0] > current_price:
                #print('Predicted: Up. Placing buy order.')
                #order_response = self.place_order(qty=100, side='buy', type='limit', time_in_force='gtc', limit_price=current_price)
                #print(f'Buy Order Response: {order_response}')
                order_response = self.api.submit_order(
                qty=100,
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
            else:
                #print('Predicted: Down. Placing short order.')
                #order_response = self.place_order(qty=100, side='sell', type='limit', time_in_force='gtc', limit_price=current_price)
                #print(f'Short Order Response: {order_response}')
                order_response = self.api.submit_order(
                qty=100,
                side='short',  # Buy the stock
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
        else:
            print('Skipping trade due to prediction error.')

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

   # def trade(self):
   #     current_price = self.api.get_latest_trade(self.symbol).price
   #     prediction = self.predict()
   #
   #     if prediction > current_price:
   #         print('Predicted: Up. Placing buy order.')
   #         order_response = self.place_order(qty=100, side='buy', type='limit', time_in_force='gtc')
   #         print(f'Buy Order Response: {order_response}')
   #     else:
   #         print('Predicted: Down. Placing short order.')
   #         order_response = self.place_order(qty=100, side='sell', type='limit', time_in_force='gtc')
   #         print(f'Short Order Response: {order_response}')

if __name__ == '__main__':
    # Replace 'your_symbol' with the symbol you want to trade (e.g., 'SPY')
    trader = ARIMATrader(symbol='SPY', path_to_data='C:\\Users\\sbrus\\Downloads\\SPY.csv')

    trader.trade()
