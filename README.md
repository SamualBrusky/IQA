# IQA
Trading Analyzer for $SPY. This is a combination of different ideas like [Bracket_Order](https://github.com/SamualBrusky/IQA/blob/main/ECON/Bracket_Order_TSLA.py) and ARMA_SPY.

# Requirements
 - [Alpaca.API](https://github.com/alpacahq/alpaca-trade-api-python)
 - [StatsModels](https://github.com/statsmodels/statsmodels)
 - import json
import os
from math import sqrt
import requests

# Third Party
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from pandas import DataFrame
from sklearn.metrics import mean_squared_error
import alpaca_trade_api as tradeapi
