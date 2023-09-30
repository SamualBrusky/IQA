import alpaca_trade_api as tradeapi
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
# Split Data into Training and Testing Sets:
from sklearn.model_selection import train_test_split


api = tradeapi.REST('<YOUR_API_KEY_ID>', '<YOUR_API_SECRET_KEY>', base_url='<API_BASE_URL>')

# Example: Get historical data for Apple Inc. (AAPL)
symbol = 'AAPL'
timeframe = '1D'  # 1 day timeframe

historical_data = api.get_barset(symbol, timeframe, limit=1000).df[symbol]

X = historical_data[['open', 'high', 'low', 'volume']]  # Use relevant features
y = historical_data['close']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)

