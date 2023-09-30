# Importing the api and instantiating the rest client according to our keys
import random
import alpaca_trade_api as api
from alpaca_trade_api import REST
import numpy as np
import pandas as pd
from alpaca.data.live.stock import StockDataStream

APCA_API_KEY_ID = 'PKUZ2L3UZHWU015HWQ7A'
API_SECRET = 'd5egbn3MDM7aiSzhlIfezlHr6EZJsFCzDcyRqfes'
BASE_URL = 'https://paper-api.alpaca.markets'

alpaca = api.REST(APCA_API_KEY_ID, API_SECRET, BASE_URL)

symbol = 'TSLA'
symbol_bars = REST.get_bars_iter(symbol, 'minute', 1).df.iloc[0]
symbol_price = symbol_bars[symbol]['close']

# A bracket buy order for $NVDA that takes profit at a 10% gain, or submits a market sell at -5% loss
symbol = symbol
qty = 10
type = "market"
order_class = "bracket"
take_profit = {"limit_price": symbol_price * 1.10}    # 10% gain sets this value to $275
stop_loss = {"stop_price": symbol_price * 0.95}       # 5% loss sets this value to $237.50
client_order_id=f"gcos_{random.randrange(100000000)}"
client_order_id = alpaca

alpaca.submit_order(
                    symbol,
                    qty=qty, 
                    type=type,
                    order_class=order_class,
                    take_profit=take_profit,
                    stop_loss=stop_loss,
                    client_order_id=client_order_id
)