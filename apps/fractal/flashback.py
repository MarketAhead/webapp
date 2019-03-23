import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from plotly import tools

import pandas as pd
import numpy as np 

from talib.abstract import *

from apps.error_page import error
from apps.prices.prices import get_price
from apps.prices.crypto import crypto_tickers

from apps.fractal.corrfinder import get_plot_dates

colorway = ["#424ff9","#ec3a1c","#00cc96","#cfa5fc","#9aebfa","#f6c6fd","#fecb52","#ffa15a","#ff6692","#b6e880"]

filtert = {'D':'Day', 'W':'Week', 'M':'Month'}
filtert_text = {'D':'Daily', 'W':'Weekly', 'M':'Monthly'}

INCREASING_COLOR = '#00cc96'
DECREASING_COLOR = '#EF553B'

def get_volumebar_colors(df):
    colors = []

    for i in range(len(df.close)):
        if i != 0:
            if df.close[i] > df.close[i-1]:
                colors.append(INCREASING_COLOR)
            else:
                colors.append(DECREASING_COLOR)
        else:
            colors.append(DECREASING_COLOR)

    return colors

def candlestick_trace(df, ticker, xindex, yaxis):
    return go.Candlestick(
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        x=df[xindex],
        yaxis = yaxis,
        increasing=dict(line=dict(color=INCREASING_COLOR)),
        decreasing=dict(line=dict(color=DECREASING_COLOR)),
        name=ticker
    )

def trace_close(df, close_col):
    
    hovertext = df['date'].apply(lambda x: x.strftime('%Y-%m-%d')).astype(str) + ': $'+ df[close_col].apply(lambda x: round(x,2)).astype(str)

    return go.Scatter(
        x = df['date'],
        y = df[close_col],
        text = hovertext,
        hoverinfo = 'text',
        mode = 'lines',
        line = dict(width=1, color=('#666')),
        name = '',
        yaxis = 'y2',
    )

def trace(df, column, name, width, xaxis, yaxis, hovertext):
    
    if hovertext:
        hovertext = df['date'].apply(lambda x: x.strftime('%Y-%m-%d')).astype(str) + ': '+ df[column].apply(lambda x: round(x,3)).astype(str) + '%'
    else:
        hovertext=''

    if xaxis == 'num':
        x = list(range(0, len(df.index)))
    elif xaxis == 'date':
        x = df['date']

    return go.Scatter(
        x = x,
        y = df[column],
        text = hovertext,
        hoverinfo = 'text',
        mode = 'lines',
        line = dict(width=width),
        name = name,
        yaxis = yaxis,
    )

def get_annotations(date, price, corr, index):
    return dict(
        x=date,
        y=price,
        xref='x',
        yref='y2',
        text=' Corr: '+ str(corr),
        showarrow=True,
        arrowhead=0,
        arrowcolor=colorway[index],
        font=dict(color='#FFF', size=12, family='Segoe UI, Arial'),
        bgcolor=colorway[index],
        ax=0,
        ay=-30-(60/(index+1)),
        arrowwidth=1
        )

def get_layout_main(ticker, annotations, ytitle, ytitle2):
    return go.Layout(
            title= '',
            titlefont=dict(size = 28),
            yaxis= dict(domain=[0, 0.15], title=ytitle,showticklabels=False, side='left', zeroline=False),
            yaxis2 = dict(domain=[0.15, 1], title=ytitle2, zeroline=False),
            xaxis= dict(zeroline=False, rangeslider=dict(visible=False),
                        showspikes = True, 
                        spikethickness = 1,
                        spikedash = "solid",
                        spikecolor = "#999",
                        spikemode = "across"
                        ),

            showlegend=False,
            annotations=annotations,
            colorway=colorway
            )

def get_layout(ticker, annotations, ytitle, xtitle):
    return go.Layout(
            title= ticker,
            yaxis= dict(title=ytitle, side='left', zeroline=False),
            xaxis= dict(title=xtitle, zeroline=False, rangeslider=dict(visible=False)),
            legend= dict(orientation='h', y=1, x=0, yanchor='bottom'),
            annotations=annotations,
            colorway=colorway
            )


def generate_flashback(ticker, window, timeRes, fractal, setDate):

    #Get Price Data
    pdata = get_price(ticker, timeRes)

    if pdata is not None:

        if ticker in crypto_tickers.keys():
            close_col = 'close'
        else:
            close_col = 'adjclose'

        if fractal == 'close':
            fractal_col = close_col
        else:
            fractal_col = fractal

        top_dates = get_plot_dates(pdata, fractal_col, setDate, window, timeRes)

        annotations = []
        for i in range(6):
            date = top_dates.iloc[i]['date']
            price = top_dates.iloc[i][close_col]
            corr = round(top_dates.iloc[i]['corr_sum'],3)
            annotations.append(get_annotations(date, price, corr, i))

        corr_plots = []
        corr_plots2 =[]
        corr_plots3 =[]

        #Candlestick comparison figure
        fig = tools.make_subplots(rows=6, cols=1, shared_xaxes=True, shared_yaxes=False,
                                vertical_spacing=0.01)


        for i in range(6):

            date = top_dates.iloc[i]['date'].strftime('%Y-%m-%d')
            location = pdata.index.get_loc(str(date))
            corr = round(top_dates.iloc[i]['corr_sum'],3)
            
            column = str(i)+'_norm'

            if location == len(pdata.index)-1:
                corr_data = pdata.tail(window+1).copy()
                corr_data['count'] = np.arange(len(corr_data))
                
                name = 'Now '+str(corr)
                width = 3
            else:
                corr_data = pdata[location-window:location+window+1].copy()
                corr_data['count'] = np.arange(len(corr_data))

                name = 'Corr: '+str(corr)
                width = 1

            #Cumulative percent change starting with first open price
            corr_data['agg_pct']=corr_data['close'].apply(lambda x: 100 * ((x/corr_data.iloc[0]['open'])-1) )
            
            corr_plots.append(trace(corr_data, 'agg_pct',name,width,'num','y',hovertext=True))
            corr_plots2.append(trace(corr_data,'OCP',name, width,'num', 'y',hovertext=True))
            corr_plots3.append(trace(corr_data,close_col,name, 3,'date', 'y2',hovertext=False))

         
            fig.append_trace(candlestick_trace(corr_data, name, 'count', 'y'), i+1, 1)

        
        fig['layout'].update(title=filtert_text[timeRes]+' Candlesticks',
                            yaxis= dict(title='', side='left', zeroline=False,),
                            xaxis= dict(title='', zeroline=False, rangeslider=dict(visible=False),
                            showspikes = True, 
                            spikethickness = 1,
                            spikedash = "solid",
                            spikecolor = "#999",
                            spikemode = "across"
                            ),
                            height=700
                            )

        #data = candlestick_trace(pdata, ticker, 'date', 'y2')
        data = trace_close(pdata, close_col)

        #Volume 
        # colors = get_volumebar_colors(pdata)
        # main_subplot = dict(x=pdata.index, y=pdata['volume'], marker=dict(color=colors),
        #             type='bar', yaxis='y', name='volume' 
        #             )

        output = RSI(pdata, timeperiod=14, price=close_col)

        main_subplot = dict(x=pdata.index, y=output,
            type='line', yaxis='y', name='RSI', line = dict(width=1, color=('#777')),
            )

        corr_plots3.append(data)
        corr_plots3.append(main_subplot)

        layout_main = get_layout_main(ticker, annotations, 'RSI', '')
        layout_corr = get_layout(filtert_text[timeRes]+' Cumulative % Change ('+ str(window) +' '+filtert[timeRes]+' Period)', [], 'Cumulative % Change', filtert[timeRes]+'s')
        layout_corr2 = get_layout(filtert_text[timeRes]+' % Change', [], '%', filtert[timeRes]+'s')


        body = dbc.Container(
                        [
                            dcc.Graph(figure=dict(data=corr_plots3, layout=layout_main), id="corrgraph_main"),  
                            dcc.Graph(figure=dict(data=corr_plots, layout=layout_corr), id="corrgraph"),
                            dcc.Graph(figure=dict(data=corr_plots2, layout=layout_corr2), id="corrgraph2"),
                            dcc.Graph(figure=fig, id="corrgraph_candle_compare")
                        ]
                      )
        return body
    else:
        return error


