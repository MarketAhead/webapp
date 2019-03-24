import numpy as np
import pandas as pd

import plotly.graph_objs as go

from apps.correlation.fred import get_fred_data,get_fred_series_units
from apps.correlation.gtrend import get_gtrend
from apps.prices.crypto import crypto_tickers

colorway = ["#636efa","#EF553B","#00cc96","#ab63fa","#19d3f3","#e763fa","#fecb52","#ffa15a","#ff6692","#b6e880"]


def main_line_trace(df, col_name, ticker):
    return go.Scatter(
        mode='lines',
        x=df.index, 
        y=df[col_name], 
        name=ticker, 
        yaxis='y'
    )

def line_trace(df, col, name, yaxis):
    return go.Scatter(
        mode='lines',
        x=df.index, 
        y=df[col], 
        name=name, 
        yaxis=yaxis
    )

def trend_traces(df, keywords, cdata):
	lst = []
	print(df)
	if len(keywords)>1:
		for keyword in keywords:
			print('this',keyword)
			corr = str(round(cdata.at[keyword, 'close'], 3))

			lst.append(line_trace(df, keyword, keyword+", Corr: "+corr, 'y2'))
	else:
		corr = str(round(cdata.at[keywords[0], 'close'], 3))
		lst.append(line_trace(df, keywords[0], keywords[0]+", Correlation: "+corr, 'y2'))

	return lst


def get_layout(start, end, title, yaxis2_title):
	return go.Layout(
	title = title, 
    yaxis= dict(title='Price', side='left', zeroline=False, showline=False),
    yaxis2= dict(title=yaxis2_title,overlaying='y',side='right', zeroline=False, showline=False),
    xaxis= dict(range=[start,end], rangeslider=dict(visible=False), zeroline=False, showline=False),
    legend= dict(orientation='h', y=1, x=0, yanchor='bottom'),
    margin=go.layout.Margin(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=0
    ),
    colorway=colorway
	)


def get_start_end(data, pdata):
	if data.index[0] > pdata['date'][0]:
		start = data.index[0]
		end = data.index[-1]
	else:
		start = pdata.index[0]
		end = pdata.index[-1]

	return start, end 


class Correlation:

	def __init__(self, ticker, pdata):

		self.ticker = ticker
		self.pdata = pdata

		if ticker in crypto_tickers.keys():
			close_col = 'close'
		else:
			close_col = 'adjclose'

		self.data_main = main_line_trace(self.pdata, close_col, ticker)

	def get_main(self):
		start = self.pdata.index[0]
		end = self.pdata.index[-1]
		title = ''
		units = ''

		layout = get_layout(start,end,title,units)

		return go.Figure(data=[self.data_main], layout=layout)


	def get_fred(self, fred):

		fdata = get_fred_data(fred)

		cdata = pd.merge(self.pdata, fdata, left_index=True, right_index=True)
		cdata = cdata.corr()

		corr = str(round(cdata.at[fred, 'close'], 3))

		datat = [line_trace(fdata, fred, fred+", Correlation: "+corr, 'y2')]
		datat.insert(0, self.data_main)

		units = get_fred_series_units(fred)

		start, end = get_start_end(fdata, self.pdata)
		title = self.ticker +' vs ' + fred

		layout = get_layout(start,end,title,units)

		return go.Figure(data=datat, layout=layout)


	def get_gtrend(self, gtrend, geo):

		print("gtrend", gtrend)

		if gtrend is not None:
			gtrend = gtrend.split(",")

		gdata = get_gtrend(gtrend, geo)

		cdata = pd.merge(self.pdata, gdata, left_index=True, right_index=True)
		cdata = cdata.corr()

		datat = trend_traces(gdata, gtrend, cdata)
		datat.insert(0, self.data_main)

		start, end = get_start_end(gdata, self.pdata)

		title = self.ticker +' vs Google Trends: ' + ','.join(gtrend)
		layout = get_layout(start, end, title, 'Trend')
		return go.Figure(data=datat, layout=layout)




