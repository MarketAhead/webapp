import pandas as pd
import numpy as np

import os
from app import app,cache

TIMEOUT = 86400
TIMEOUT_LONG = 604800

from fredapi import Fred
fred = Fred(api_key=os.environ['FRED_KEY'])

def get_fred_series_units(series_id):

	try:
		result = fred.search(series_id)
		units = result['units_short'].loc[series_id]

		return units
	except:
		print('error fred units')
		return series_id

@cache.memoize(timeout=TIMEOUT)
def search_fred(search):
	try:
		result = fred.search(search)

		result = result.head(50).to_json(orient='records')

		return result
	except:
		print('error')
		return None

@cache.memoize(timeout=TIMEOUT)
def get_fred_data(series_id):

	fdata = fred.get_series(series_id)
	
	unsampled = fdata.resample('D')
	interpolated = unsampled.interpolate(method='linear')

	fdata = pd.DataFrame({'date':pd.to_datetime(interpolated.index), 'value':interpolated.values}) 

	fdata.set_index('date',drop=True, inplace=True)
	fdata.rename(columns={'value': series_id}, inplace=True)

	return fdata

if __name__ == "__main__":
	# print (get_fred_series())
	search_fred('korea housing')