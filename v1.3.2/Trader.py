import os
import json
import requests
from alpaca_trade_api import REST, TimeFrame
import subprocess
import alpaca_trade_api as tradeapi
from datetime import datetime, timedelta

# Alpaca API credentials
APCA_API_KEY_ID = 'PKDWJ6MXKGXRG6HTPDPP'
APCA_API_SECRET_KEY = 'xmFzrJDkVU2KW9C2tafwCsNggeLqxSphuaRdRqah'
BASE_URL = 'https://paper-api.alpaca.markets'
ORDERS_URL = f'{BASE_URL}/v2/orders'
HEADERS = {'APCA-API-KEY-ID': APCA_API_KEY_ID, 'APCA-API-SECRET-KEY': APCA_API_SECRET_KEY}

api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, BASE_URL)

# Function to get stock data
def get_stock_data(symbol, start_date, end_date):
    rest_client = REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY)
    data = rest_client.get_bars(symbol, TimeFrame.Day, start_date, end_date).df
    return data.to_json()

# Function to run R script for ARIMA prediction
def run_r_script():
    r_script_path = r"C:\\Program Files\\R\\R-4.3.3\\bin\\Rscript.exe"
    prediction_script_path = r"C:\\Users\\sbrus\\OneDrive\\Documents\\GitHub\\Fiequn.com\\ECON\\v1.3.0\\Prediction.R"
    subprocess.run([r_script_path, prediction_script_path])

# Function to read prediction from file
def read_prediction_from_file(filename):
    try:
        with open(filename, 'r') as f:
            prediction = f.read()
        return prediction
    except FileNotFoundError:
        return None

# Function to submit order
def submit_order(data):
    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)
    return json.loads(r.content)

# Function to place order
def place_order(symbol, qty, side, type, time_in_force, order_class, limit_price):
    data = {
        'symbol': symbol,
        'qty': qty,
        'side': side,
        'type': type,
        'time_in_force': time_in_force,
        'order_class': order_class,
        'limit_price': limit_price
    }
    return submit_order(data)

# Function to trade based on prediction
# Function to trade based on prediction
def trade(current_price, prediction):
    if prediction:
        prediction_price = float(prediction[0])  # Get the first prediction value
        tick_size = 0.01
        base_price = current_price

        take_profit_price = max(base_price + 1, round(current_price * 1.001, -1))  # Round to five decimal places (cents)
        stop_loss_price = max(base_price - 1, round(current_price * 0.999, 1))  # Round to five decimal places (cents)
        
        if take_profit_price <= stop_loss_price:
            take_profit_price = stop_loss_price + 0.01

        print(f"Current Price: {current_price}")
        print(f"Predicted Price: {prediction_price}")
        print(f"Take Profit Price: {take_profit_price}")
        print(f"Stop Loss Price: {stop_loss_price}")

        if prediction_price > current_price:
            side = 'buy'
        else:
            side = 'sell'

        order_data = {
            'symbol': symbol,
            'qty': 200,
            'side': side,
            'type': 'limit',
            'time_in_force': 'gtc',
            'limit_price': current_price,
            'order_class': 'bracket',
            'take_profit': {
                'limit_price': take_profit_price
            },
            'stop_loss': {
                'stop_price': stop_loss_price,
                'limit_price': stop_loss_price  # Sell at market if the price drops below stop-loss
            }
        }
        order_response = submit_order(order_data)
        print("Order response:", order_response)
    else:
        print("Prediction not available.")



if __name__ == '__main__':
    # Define parameters
    symbol = 'SPY'
    start_date = (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')  # Start date 180 days ago
    end_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    # Get stock data and write to file
    stock_data = get_stock_data(symbol, start_date, end_date)
    with open('stock_data.json', 'w') as f:
        f.write(stock_data)

    # Run R script for ARIMA prediction
    run_r_script()

    # Check if prediction file exists and read prediction from file
    prediction_file = 'prediction.txt'
    prediction = read_prediction_from_file(prediction_file)

    # Placeholder for current price
    current_price = api.get_latest_trade(symbol).price
    
    if prediction:
        trade(current_price, prediction.split('\n'))  # Passing the prediction values as a list
        print("Prediction: ", prediction)
    else:
        print("Prediction file not found. The R script may have encountered an error.")
