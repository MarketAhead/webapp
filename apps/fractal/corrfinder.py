import pandas as pd
import numpy as np

def get_window(win, len_windows):
	windows = []
	windows.append(win)

	for i in range(len_windows-1):
		windows.append((i+1)*(win/len_windows))

	windows = [int(x) for x in windows]

	return sorted(windows, key=int)

def get_len_windows(win):
	if win <= 10:
		return 1
	#Window length of 3 seems good for smaller windows
	if win <=20:
		return 3
	else:
		return 5

def get_nonoverlap_days(dates, set_date, max_window):
	top_corr_dates = []
	top_corr_dates.append(dates[0])

	n = 0
	#Get the top 10 nonoverlap days to speed things up!
	while n < len(dates) and len(top_corr_dates)<10:

		for top_corr_date in top_corr_dates:
			# print('corr',top_corr_date,'vs set ', set_date)
			if abs(np.busday_count(top_corr_date, dates[n])) < max_window:
				flag = 0
				break
			else:
				flag = 1
		
		if flag == 1:
			top_corr_dates.append(dates[n])
		
		n+=1

	return top_corr_dates


def get_plot_dates(data, column_name, set_date, win, time_res):

	len_windows = get_len_windows(win)
	windows = get_window(win, len_windows)
	max_window = max(windows)

	for windowLength in windows:

		last = data.loc[:set_date].tail(windowLength)

		this = lambda x: np.corrcoef(last[column_name].values, x.values)[0,1] if len(set(x.values))!=1 else 0
		data[windowLength] = data[column_name].rolling(windowLength).apply(this, raw=False) 

	#Get sum of weighted corr values from windows
	data['corr_sum'] = 0

	for window in windows:
		data['corr_sum'] += data[window]*(1/len_windows) 

	sorted_data = data.sort_values(by=['corr_sum'], ascending=[False])

	all_dates = sorted_data.index.tolist()

	if time_res == 'D':
		dates = get_nonoverlap_days(all_dates, set_date, max_window)
	if time_res == 'W':
		dates = get_nonoverlap_days(all_dates, set_date, max_window)
	if time_res == 'M':
		dates = get_nonoverlap_days(all_dates, set_date, max_window)

	top_dates = sorted_data[sorted_data['date'].isin(dates)]
	     
	return top_dates

