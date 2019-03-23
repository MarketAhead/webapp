import pandas as pd
import numpy as np

import config, os
from app import app,cache

TIMEOUT = 86400
TIMEOUT_LONG = 604800

from fredapi import Fred
fred = Fred(api_key=os.environ['FRED_KEY'])

from airtable import Airtable


@cache.memoize(timeout=TIMEOUT_LONG)
def get_records():
	apiKey = os.environ['AIRTABLE_KEY']
	base_key = 'appIZ52SrHcih9DLC'
	table_name = 'Fred'

	airtable = Airtable(base_key, table_name, api_key=apiKey)
	return airtable.get_all()

def get_fred_series():

	fred_dict = {}
	records = get_records()

	for record in records:
		fred_dict.update({record['fields']['Code']:record['fields']['Indicator']})

	sorted_fred_dict = {k: v for k, v in sorted(fred_dict.items(), key=lambda x: x[1])}
	return sorted_fred_dict

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