import alpaca_trade_api as tradeapi
import math

APCA_API_KEY_ID = 'PK5D00K1N6B74HTDEYJR'
API_SECRET = '51Q5ZrtMeCkh7HWnuOIoIB2bUoA9ZcBFeSHfAlkq'
BASE_URL = 'https://paper-api.alpaca.markets'

alpaca = tradeapi.REST(APCA_API_KEY_ID, API_SECRET, BASE_URL)

symbol = 'VCIG'  # Replace with your desired stock symbol
qty = 100  # Number of shares to buy

# Get the current price of the stock
current_price = alpaca.get_latest_trade(symbol).price

# Manually set a tick size based on your understanding of the stock's trading rules
tick_size = 0.01  # Example: $0.01 tick size

take_profit_price = round(current_price * 1.001, 2)  # Round to two decimal places (cents)
stop_loss_price = round(current_price * 0.999, 2)  # Round to two decimal places (cents)

# Place the bracket order
order = alpaca.submit_order(
    symbol=symbol,
    qty=qty,
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

print("Bracket order placed:")
print("Order ID:", order.id)
print("Symbol:", order.symbol)
print("Type:", order.type)
print("Qty:", order.qty)
print("Limit Price:", order.limit_price)
print("Take Profit Price:", take_profit_price)
print("Stop Loss Price:", stop_loss_price)
