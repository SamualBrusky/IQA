import alpaca_trade_api as tradeapi
import math

APCA_API_KEY_ID = 'PKNCK38IJB8Y9JZ23KSE'
API_SECRET = 'KsxcqDsIUpf3pYUhGXACArVlSbfAZ6HdYV3yNed8'
BASE_URL = 'https://paper-api.alpaca.markets'

alpaca = tradeapi.REST(APCA_API_KEY_ID, API_SECRET, BASE_URL)

symbol = 'TSLA'
qty = 10  # Number of shares to buy

# Get the current price of the stock
current_price = alpaca.get_latest_trade(symbol).price

# Manually set a tick size based on your understanding of the stock's trading rules
tick_size = 0.01  # Example: $0.01 tick size

# Calculate the take-profit and stop-loss prices
take_profit_price = round(current_price * 1.1 / tick_size) * tick_size

# Round the stop-loss price to the nearest tick size increment
stop_loss_price = round(current_price * 0.9 / tick_size) * tick_size

# Use math.floor to round down and math.ceil to round up to the nearest cent
take_profit_price = math.floor(take_profit_price / tick_size) * tick_size
stop_loss_price = math.ceil(stop_loss_price / tick_size) * tick_size

# Check if the take profit limit price is greater than the stop loss stop price
if take_profit_price <= stop_loss_price:
    raise ValueError("Take profit limit price must be higher than stop loss stop price")

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
