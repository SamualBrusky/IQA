from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import LimitOrderRequest
from alpaca.trading.requests import StopLimitOrderRequest

API_KEY = 'PKN2IHNOQDPF2PKZ8X1U'
API_SECRET_KEY = 'IwY7lHYjVXRo7AZO7GNNWYbkgUEVOs6ChvKiCxR5'


Client = TradingClient(API_KEY, API_SECRET_KEY, paper=True)
account = dict(Client.get_account())
for k,V in account.items():
    print(f"{k:30}{V}")
