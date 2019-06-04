# -*- coding: utf-8 -*-
# testing getting an image refreshed periodically
# ross lazarus me fecit June 2019
import dash
import time
import random
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import urllib.request
import base64

refresh1 = 1200 # secs
refresh2 = 3600 # secs

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[

    dcc.Interval(
            id='btimer',
            interval=refresh1*1000 ,
            disabled=False,
            n_intervals=0
            ),
    dcc.Interval(
            id='ptimer',
            interval=refresh2*1000 ,
            disabled=False,
            n_intervals=0
            ),

#buttons.webcam4 = {width:12, isimage:true, refresh:600,
# image: 'http://203.217.21.105:1050/jpg/1/image.jpg', url: 'http://203.217.21.105:1050/view/viewer_index.shtml'};


    html.H1(children='Francis St. and environs',style={'color': 'darkblue', 'fontSize': 20, 'text-align':'center'}),

    html.Table( children=[
        html.Tr('Test table layout',style={'color': 'darkblue', 'fontSize': 15, 'text-align':'center'}),
        html.Tr([
            html.Td(
            html.Img( id="bbeach",
                width=400,height=300,
                src = "http://webcams.bsch.com.au/bondi_beach/1252x940.jpg?cache=%d" % random.randint(0,30000)
                )),
            html.Td(
            html.Img( id="icebergs",
                width=400,height=300,
                src = "http://203.217.21.105:1050/jpg/1/image.jpg?cache=%d" % random.randint(0,30000)
                )),
            html.Td(
            html.Img( id="big",
                width=400,height=300,
                src = "http://192.168.1.108/snapshot.jpg"
                ))], style = {'display': 'block'}),
        html.Tr([
            html.Td(
            html.Img( id="small",
                width=400,height=300,
                src = "http://192.168.1.107/snapshot.jpg"
                )),
            html.Td(
            html.Img( id="pi1",
                width=500,height=400,
                src = "http://192.168.1.199/"
                )),
            html.Td(
            html.Img( id="pi2",
                width=500,height=400,
                src = "http://192.168.1.200/"
                ))], style = {'display': 'block'} ),
            ])
        ])

@app.callback([Output('bbeach','src'),Output('icebergs','src'),Output('big','src'),Output('small','src')],
              [Input('btimer', 'n_intervals')])
def display_beach(n_intervals):
    sbb = "http://webcams.bsch.com.au/bondi_beach/1252x940.jpg?cache=%d" % random.randint(0,30000)
    sice = "http://203.217.21.105:1050/jpg/1/image.jpg?cache=%d" % random.randint(0,30000)
    sbig = "http://192.168.1.108/snapshot.jpg"
    ssmall = "http://192.168.1.107/snapshot.jpg"
    print('Four updated',time.strftime('%H:%M:%S'),'n_intervals',n_intervals)
    return sbb,sice,sbig,ssmall

@app.callback([Output('pi1','src'),Output('pi2','src')],
              [Input('ptimer', 'n_intervals')])
def display_pis(n_intervals):
    sp1 = "http://192.168.1.199/"
    sp2 = "http://192.168.1.200/"
    print('pis updated',time.strftime('%H:%M:%S'),'n_intervals',n_intervals)
    return sp1,sp2

if __name__ == '__main__':
    app.run_server(debug=True)
