import yfinance as yf
import pandas as pd 

dataF = yf.download("EURUSD=X", start ="2023-7-5", end="2023-7-21", interval='15m')
dataF.iloc[-1:,:]
dataF.Open.iloc