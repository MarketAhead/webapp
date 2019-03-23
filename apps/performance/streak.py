import numpy as np
import pandas as pd

import plotly.graph_objs as go
import dash_table

from apps.prices.crypto import crypto_tickers


colorway = ["#636efa","#EF553B","#00cc96","#ab63fa","#19d3f3","#e763fa","#fecb52","#ffa15a","#ff6692","#b6e880"]

def main_line_trace(df, col_name, ticker):
    return go.Scatter(
        mode='lines',
        x=df.index, 
        y=df[col_name], 
        name=ticker, 
        line = dict(width=1, color=('#666')),
        yaxis='y'
    )

def get_layout(annotations):
	return go.Layout(
	title = '', 
	yaxis= dict(title='Price',showticklabels=True, side='left', zeroline=False),

    xaxis= dict(zeroline=False, rangeslider=dict(visible=False)),

	annotations=annotations,
	showlegend=False,    
	colorway=colorway
	)

def get_annotations(date, price, index):
    return dict(
        x=date,
        y=price,
        xref='x',
        yref='y',
        text=' '+str(index+1)+' ',
        showarrow=True,
        arrowhead=0,
        arrowcolor=colorway[index],
        font=dict(color='#FFF', size=12, family='Segoe UI, Arial'),
        bgcolor=colorway[index],
        ax=0,
        ay=-30-(60/(index+1)),
        arrowwidth=1
        )

def get_table(df, columns):

	return dash_table.DataTable(
        id='datatable-paging',
	    data=df.to_dict('rows'),
	    columns = columns, 
	    style_as_list_view=True,
	    style_cell={'padding': '5px', 'text-align':'left'},
	    style_header={
	        'backgroundColor': 'white',
	        'fontWeight': 'bold'
	    }, 
	    style_data_conditional=[
	 		{
	            'if': {
	                'column_id': 'rank',
	                'filter': 'rank eq num('+str(i+1)+')'
	            },
	            'color': 'white',
	            'backgroundColor': c,
	            'fontWeight': 'bold'
	        } for i, c in enumerate(colorway) 
	        ],

	    pagination_settings={
	        'current_page': 0,
	        'page_size': 20,
	        'displayed_pages': 1
	    },
		pagination_mode='fe',
	)

def create_annotations(data, close_col):

	annotations = []

	for i in range(10):

	    date = data.iloc[i]['date']
	    price = data.iloc[i][close_col]
	    annotations.append(get_annotations(date, price, i))

	return annotations

def create_streak_annotations(result, data, close_col):

	annotations = []

	#Prevent index out of bounds if less streaks than 10
	if len(result.index) < 10:
		r = len(result.index)
	else:
		r = 10

	for i in range(r):

	    date = result.iloc[i]['date']
	    print(result)
	    price = data.loc[data['date'] == date][close_col].iat[0]
	    annotations.append(get_annotations(date, price, i))

	return annotations

def trace(df, column, color):
    
    return go.Scatter(
        x = df.index.strftime('%Y-%m-%d'),
        y = df[column],
        hoverinfo = 'text',
        mode = 'lines',
        line = dict(width=3, color=color),
        yaxis = 'y',
    )

def create_traces(result, data, column):
	plots = []

	#Prevent index out of bounds if less streaks than 10
	if len(result.index) < 10:
		r = len(result.index)
	else:
		r = 10
	
	for i in range(r):
		start = result.iloc[i]['date']
		end = result.iloc[i]['end']
		color = colorway[i]

		sdata = data.loc[start:end]
		plots.append(trace(sdata, column, color))

	return plots


class Streak:

	def __init__(self, ticker, data, timeres):

		if ticker in crypto_tickers.keys():
			close_col = 'close'
		else:
			close_col = 'adjclose'

		self.close_col = close_col

		self.ticker = ticker
		self.data_main = main_line_trace(data, close_col, ticker)

		self.layout = get_layout([])
		self.table = []

		data['Last Close'] = data['close'].shift(1)
		data['LAC_OP']= 100*(data['open']-data['Last Close'])/data['Last Close']

		data['sign'] = np.sign(data['close'] - data['open'])
		data['value_grp'] = (data.sign.diff(1) != 0).astype('int').cumsum()
		data['ddate_dm'] = data['date'].dt.strftime("%B %d, %Y")
		data['ddate'] = data['date'].dt.strftime("%B, %Y")


		result = pd.DataFrame({'date': data.groupby('value_grp').date.first(),
		              'ddate': data.groupby('value_grp').date.first().dt.strftime("%B, %Y"),
		              'ddate_dm': data.groupby('value_grp').date.first().dt.strftime("%B %d, %Y"),
		              'end' : data.groupby('value_grp').date.last(),
		              'dend' : data.groupby('value_grp').date.last().dt.strftime("%B %d, %Y"),
					  'Streak' : data.groupby('value_grp').size(),
		              'Start Price': data.groupby('value_grp').open.first(),
		              'End Price': data.groupby('value_grp').close.last(),
		              }).reset_index(drop=True)


		result['Percent Change'] = 100*(result['End Price']-result['Start Price'])/result['Start Price']
		
		if timeres == 'M':
			self.ddate = 'ddate'
		else:
			self.ddate = 'ddate_dm'

		data.index = pd.to_datetime(data.index)

		self.data = data.round(2)
		self.result = result.round(2)


	def get_win_all(self):
		result = self.data.sort_values('OCP', ascending=False)
		result = result[result['OCP']>0] 
		result['rank'] = range(1,len(result)+1)

		annotations = create_annotations(result, self.close_col)
		self.layout = get_layout(annotations)

		columns = [
			{'id': 'rank', 'name':'Rank'},
			{'id': self.ddate, 'name':'Date'},
			{'id': 'OCP', 'name':'% Change'},
			{'id': 'open', 'name':'Open'},
			{'id': 'close', 'name':'Close'}
			]
		self.table =  get_table(result, columns)

	def get_loss_all(self):
		result = self.data.sort_values('OCP', ascending=True)
		result = result[result['OCP']<0] 
		result['rank'] = range(1,len(result)+1)

		annotations = create_annotations(result, self.close_col)
		self.layout = get_layout(annotations)

		columns = [
			{'id': 'rank', 'name':'Rank'},
			{'id': self.ddate, 'name':'Date'},
			{'id': 'OCP', 'name':'% Change'},
			{'id': 'open', 'name':'Open'},
			{'id': 'close', 'name':'Close'}
			]
		self.table =  get_table(result, columns)

	def get_win_all_ah(self):
		result = self.data.sort_values('LAC_OP', ascending=False)
		result = result[result['LAC_OP']>0]
		result['rank'] = range(1,len(result)+1)
  

		annotations = create_annotations(result, self.close_col)
		self.layout = get_layout(annotations)

		columns = [
			{'id': 'rank', 'name':'Rank'},
			{'id': self.ddate, 'name':'Date'},
			{'id': 'LAC_OP', 'name':'% AH Change'},
			{'id': 'open', 'name':'Open'},
			{'id': 'Last Close', 'name':'Previous Close'},
			]
		self.table =  get_table(result, columns)

	def get_loss_all_ah(self):
		result = self.data.sort_values('LAC_OP', ascending=True)
		result = result[result['LAC_OP']<0]
		result['rank'] = range(1,len(result)+1)
 

		annotations = create_annotations(result, self.close_col)
		self.layout = get_layout(annotations)

		columns = [
			{'id': 'rank', 'name':'Rank'},
			{'id': self.ddate, 'name':'Date'},
			{'id': 'LAC_OP', 'name':'% AH Change'},
			{'id': 'open', 'name':'Open'},
			{'id': 'Last Close', 'name':'Previous Close'}
			]
		self.table =  get_table(result, columns)

	###################

	###################

	def get_win_streak(self): 
		result = self.result.sort_values('Streak', ascending=False)
		result = result[result['Percent Change']>0] 
		result['rank'] = range(1,len(result)+1)

		annotations = create_streak_annotations(result, self.data, self.close_col)
		self.layout = get_layout(annotations)

		columns = [
			{'id': 'rank', 'name':'Rank'},
			{'id': self.ddate, 'name':'Start'},
			{'id': 'dend', 'name':'End'},
			{'id': 'Streak', 'name':'Streak'},
			{'id': 'Percent Change', 'name':'% Change'},
			{'id': 'Start Price', 'name':'Start Price'},
			{'id': 'End Price', 'name':'End Price'},
			]
		self.table =  get_table(result, columns)

		traces = create_traces(result, self.data, self.close_col)
		traces.insert(0, self.data_main)
		self.data_main = traces


	def get_loss_streak(self):
		result = self.result.sort_values('Streak', ascending=False)
		result = result[result['Percent Change']<0]
		result['rank'] = range(1,len(result)+1)
 

		annotations = create_streak_annotations(result, self.data, self.close_col)
		self.layout = get_layout(annotations)

		columns = [
			{'id': 'rank', 'name':'Rank'},
			{'id': self.ddate, 'name':'Start'},
			{'id': 'dend', 'name':'End'},
			{'id': 'Streak', 'name':'Streak'},
			{'id': 'Percent Change', 'name':'% Change'},
			{'id': 'Start Price', 'name':'Start Price'},
			{'id': 'End Price', 'name':'End Price'},
			]
		self.table =  get_table(result, columns)

		traces = create_traces(result, self.data, self.close_col)
		traces.insert(0, self.data_main)
		self.data_main = traces

	def get_win_perc_streak(self):
		result = self.result.sort_values('Percent Change', ascending=False)
		result = result[result['Percent Change']>0] 
		result['rank'] = range(1,len(result)+1)


		annotations = create_streak_annotations(result, self.data, self.close_col)
		self.layout = get_layout(annotations)

		columns = [
			{'id': 'rank', 'name':'Rank'},
			{'id': self.ddate, 'name':'Start'},
			{'id': 'dend', 'name':'End'},
			{'id': 'Percent Change', 'name':'% Change'},
			{'id': 'Streak', 'name':'Streak'},
			{'id': 'Start Price', 'name':'Start Price'},
			{'id': 'End Price', 'name':'End Price'},
			]
		self.table =  get_table(result, columns)

		traces = create_traces(result, self.data, self.close_col)
		traces.insert(0, self.data_main)
		self.data_main = traces

	def get_loss_perc_streak(self):
		result = self.result.sort_values('Percent Change', ascending=True)
		result = result[result['Percent Change']<0]
		result['rank'] = range(1,len(result)+1)

		annotations = create_streak_annotations(result, self.data, self.close_col)
		self.layout = get_layout(annotations)

		columns = [
			{'id': 'rank', 'name':'Rank'},
			{'id': self.ddate, 'name':'Start'},
			{'id': 'dend', 'name':'End'},
			{'id': 'Percent Change', 'name':'% Change'},
			{'id': 'Streak', 'name':'Streak'},
			{'id': 'Start Price', 'name':'Start Price'},
			{'id': 'End Price', 'name':'End Price'},
			]
		self.table =  get_table(result, columns) 

		traces = create_traces(result, self.data, self.close_col)
		traces.insert(0, self.data_main)
		self.data_main = traces
