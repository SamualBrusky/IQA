import alpaca_trade_api as tradeapi
import time

# Set up your Alpaca paper trading API credentials
api_key = 'PKZZCQDSHZAHMY7HPLQE'
api_secret = 'bh1ee30Jub8rKWsOzeaKihxGiPn6aimHupmefyl3'
base_url = 'https://paper-api.alpaca.markets'

# Create an Alpaca API connection
api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

# Define the stock symbol you want to trade
symbol = 'AAPL'

# Define your trading strategy (e.g., SMA crossover)
def simple_sma_crossover(symbol, short_sma_period, long_sma_period):
    # Get historical data
    historical_data = api.get_barset(symbol, 'day', limit=long_sma_period).df[symbol]

    # Calculate short-term and long-term SMAs
    short_sma = historical_data['close'].rolling(window=short_sma_period).mean()
    long_sma = historical_data['close'].rolling(window=long_sma_period).mean()

    # Check if the short-term SMA crosses above the long-term SMA
    if short_sma[-1] > long_sma[-1] and short_sma[-2] <= long_sma[-2]:
        return True
    else:
        return False

# Main trading loop
while True:
    if simple_sma_crossover(symbol, 50, 200):
        # Place a buy order when the crossover condition is met
        api.submit_order(
            symbol=symbol,
            qty=1,  # Number of shares to buy
            side='buy',
            type='market',
            time_in_force='gtc'
        )
        print(f"Bought 1 share of {symbol}")
    
    time.sleep(3600)  # Sleep for 1 hour before checking again (adjust as needed)
