# First Party
import json
import os
from math import sqrt
import requests

# Third Party
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from pandas import DataFrame
from sklearn.metrics import mean_squared_error
import alpaca_trade_api as tradeapi
import numpy as np

#Data


BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
HEADERS = {'PKFQM1PVOX0PAU912RL7': os.getenv('PKFQM1PVOX0PAU912RL7'), 'ny42XrA0irhWH6iBhignGaHFokP1hPjtCpX1gwMe': os.getenv('ny42XrA0irhWH6iBhignGaHFokP1hPjtCpX1gwMe')}

class Analyzer:
    def __init__(self, pathToData: str) -> None:
        super().__init__()
        self.api = tradeapi.REST()
        self.predictions = list()
        self.df = pd.read_csv(pathToData, index_col=0, parse_dates=True)
        self.model = ARIMA(self.df.High, order=(5, 1, 0))
        self.model_fit = self.model.fit()

    def __str__(self) -> str:
        return str(self.model_fit.summary())

    def get_residuals(self):
        residuals = DataFrame(self.model_fit.resid)
        return residuals.describe()

    def split_data(self, split_proportion=0.7):
        data = self.df.High.values
        size = int(len(data) * split_proportion)
        train, test = data[0:size], data[size:len(data)]
        return [train, test]

    def train_and_predict(self, train_data, test_data):
        history = [x for x in train_data]
        i = 0;
        for t in range(len(test_data)):
            model = ARIMA(history, order=(5, 1, 0))
            model_fit = model.fit()
            output = model_fit.forecast()
            y_hat = output[0]

            if i % 1000 == 0 and i != 0:
                [open, close] = self.get_current_day_price('GOOGL')
                if y_hat > open:
                    print('Execute order! 🏦🏦🏦🏦')
                    self.create_order('SPY', 100, 'buy', 'market', 'gtc')
                else:
                    print('Buy if you wanna lose money, that is why im shorting $SPY')
                    self.create_order('SPY', 100, 'short', 'market', 'gtc')
            
            


            self.predictions.append(y_hat)
            obs = test_data[t]
            history.append(obs)
            print('predicted=%f, expected=%f' % (y_hat, obs))
            i += 1

        rmse = sqrt(mean_squared_error(test_data, self.predictions))
        print('Test RMSE: %.3f' % rmse)


    def create_order(self, symbol, qty, side, type, time_in_force):
        data = {
            "symbol": symbol,
            "qty": qty,
            "side": side,
            "type": type,
            "time_in_force": time_in_force
        }

        r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

        return json.loads(r.content)

    def get_orders(self):
        r = requests.get(ORDERS_URL, headers=HEADERS)
        return json.loads(r.content)

    def get_current_day_price(self, symbol):
        barset = self.api.get_barset(symbol, 'day', limit=1)
        bars = barset[symbol]

        open = bars[0].o
        close = bars[-1].c
        return [open, close]


if __name__ == '__main__':
    analyzer = Analyzer("C:\\Users\\sbrus\\OneDrive\\Social Network\\TestWebsite-1\\facial tracker\\.vscode\\ECON\\S&P500_6M_Data.csv")
    [train, test] = analyzer.split_data()
    analyzer.train_and_predict(train, test)


