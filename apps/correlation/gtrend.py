import pandas as pd
import numpy as np

from pytrends.request import TrendReq

def get_gtrend(name, geo):

	pytrend = TrendReq()
	pytrend.build_payload(kw_list=name,geo=geo)

	# Interest Over Time
	gtrend_data = pytrend.interest_over_time()

	# Daily Gtrend
	unsampled = gtrend_data.resample('D')
	interpolated_data = unsampled.interpolate(method='linear')
	
	return interpolated_data

