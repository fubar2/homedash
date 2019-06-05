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

hour3 = 1200 # secs
hour1 = 3600 # secs

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

  
def generate_table(urls):
    return html.Table(
        # Header
        # [html.Tr([html.Th(t) for t in titles)] +

        # Body
        [html.Tr([
            html.Td(html.Img(
                width=400,#height=300,
                src = urls[i])) for i in range(len(urls))]
        )])

def geth1():
    return generate_table(["http://192.168.1.199/?cache=%d" % random.randint(0,30000),
    "http://192.168.1.200/?cache=%d" % random.randint(0,30000)])
    
def geth3():
    return generate_table(["http://203.217.21.105:1050/jpg/1/image.jpg?cache=%d" % random.randint(0,30000),
    "http://webcams.bsch.com.au/bondi_beach/1252x940.jpg?cache=%d" % random.randint(0,30000),
    "http://192.168.1.108/snapshot.jpg?cache=%d" % random.randint(0,30000),
    "http://192.168.1.107/snapshot.jpg?cache=%d" % random.randint(0,30000)])
  
        
app = dash.Dash(__name__) #, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[

    dcc.Interval(
            id='btimer',
            interval=hour3*1000 ,
            n_intervals = 0
            ),
    dcc.Interval(
            id='ptimer',
            interval=hour1*1000 ,
            n_intervals = 0
            ),

    html.Div(id = "h3im", children=[
        geth3()
        ]),
        
    html.Div(id = "h1im", children=[
        geth1()
        ])
    ])

@app.callback(Output('h3im','children'),
            [Input('btimer', 'n_intervals')])
def display_hour3(n_intervals):
    t = geth3()
    print('Hour3 images updated',time.strftime('%H:%M:%S'),'n_intervals',n_intervals)
    return t

@app.callback(Output("h1im",'children'),
            [Input('ptimer', 'n_intervals')])
def display_hour(n_intervals):
    print('Hour1 images updated',time.strftime('%H:%M:%S'),'n_intervals',n_intervals)
    t = geth1()
    return t
    
if __name__ == '__main__':
    app.run_server(debug=True)
