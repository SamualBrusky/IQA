import requests 

def get_date_bars(ticker_symbol, open_timestamp, close_timestamp):

    # set the url for pulling bar data
    base_url = 'https://data.alpaca.markets/v1/bars/minute'

    # set the request headers using our api key/secret
    request_headers = {'APCA-API-KEY-ID': '<YOUR_KEY_HERE>', 'APCA-API-SECRET-KEY': '<YOUR_SECRET_HERE>'}

    # set the request params for the next request
    request_params = {'symbols': ticker_symbol, 'limit': 1000, 'start': open_timestamp.isoformat(), 'end': close_timestamp.isoformat()}

    # get the response
    date_bars = requests.get(base_url, params=request_params, headers=request_headers).json()[ticker_symbol]

    # if the date on the response matches the closing date for the day, throw the candle away (since it technically happens after the close)
    if date_bars[-1]['t'] == int(close_timestamp.timestamp()):
        date_bars = date_bars[:-1]

    # return the bars for the date
    return date_bars

