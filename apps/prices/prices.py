import pandas as pd
import numpy as np

from alpha_vantage.cryptocurrencies import CryptoCurrencies
from alpha_vantage.timeseries import TimeSeries

import os
from apps.prices.crypto import crypto_tickers

from datetime import datetime,timedelta
today = datetime.now()

from app import app,cache
TIMEOUT = 3600

ALPHA_KEY = os.environ['ALPHA_KEY']  

def get_crypto(ticker, time_res):
	try:
		cc = CryptoCurrencies(key=ALPHA_KEY, output_format='pandas')

		if time_res == 'D':
			data, meta_data = cc.get_digital_currency_daily(symbol=ticker, market='USD')
		if time_res == 'W':
			data, meta_data = cc.get_digital_currency_weekly(symbol=ticker, market='USD')
		if time_res == 'M':
			data, meta_data = cc.get_digital_currency_monthly(symbol=ticker, market='USD')

		data.rename(index=str, 
	               columns={'1a. open (USD)':'open',
	               '2a. high (USD)':'high',
	               '3a. low (USD)':'low',
	               '4a. close (USD)':'close',
	               '5. volume':'volume',
	               '6. market cap (USD)':'marketcap',
	               }, inplace=True)

		data.drop(['1b. open (USD)','2b. high (USD)','3b. low (USD)','4b. close (USD)'], 
		          axis=1, inplace=True)

		return data

	except:
		print("Can't get crypto data")
		return None

def get_stock(ticker, time_res):
	try:
		ts = TimeSeries(key=ALPHA_KEY, output_format='pandas')
		if time_res == 'D':
			data, meta_data = ts.get_daily_adjusted(symbol=ticker, outputsize='full')
		if time_res == 'W':
			data, meta_data = ts.get_weekly_adjusted(symbol=ticker)
		if time_res == 'M':
			data, meta_data = ts.get_monthly_adjusted(symbol=ticker)

		data.rename(index=str, 
					columns={'1. open':'open',
					'2. high':'high',
					'3. low':'low',
					'4. close':'close',
					'5. adjusted close': 'adjclose',
					'6. volume':'volume',
					}, inplace=True)

		return data

	except:
		print("Can't get stock data")
		return None

@cache.memoize(timeout=TIMEOUT)
def get_price(ticker, time_res):
	if ticker in crypto_tickers.keys():
		data = get_crypto(ticker, time_res)
	else:
		data = get_stock(ticker, time_res)

	print("Got Data!")
	data['date'] = pd.to_datetime(data.index)  
	data.set_index('date',drop=False)

	data['OCP'] = 100*(data['close']-data['open'])/data['open']
	data['CP'] = data['close'].pct_change()
	data['LHP'] = 100*(data['high']-data['low'])/data['low']

	#Clean up any bad data 
	data = data.replace(0,np.nan).ffill()
	data = data.fillna(0)

	return data

