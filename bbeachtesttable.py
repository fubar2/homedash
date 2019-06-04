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
hurls = ["http://192.168.1.199/","http://192.168.1.200/"]
h3urls = ["http://webcams.bsch.com.au/bondi_beach/1252x940.jpg?cache=%d" % random.randint(0,30000),
    "http://203.217.21.105:1050/jpg/1/image.jpg?cache=%d" % random.randint(0,30000),
    "http://192.168.1.108/snapshot.jpg",
    "http://192.168.1.107/snapshot.jpg"]
titles = ['North','Bergs','Big','Small','Pi1','Pi2']
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
                width=400,height=300,
                src = urls[i])) for i in range(len(urls))]
        )])

        
app = dash.Dash(__name__) #, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[

    dcc.Interval(
            id='btimer',
            interval=hour3*1000 ,
            ),
    dcc.Interval(
            id='ptimer',
            interval=hour1*1000 ,
            ),

    html.Div(id = "h3im", children=[
        generate_table(h3urls)
        ]),
        
    html.Div(id = "h1im", children=[
        generate_table(hurls)
        ])
    ])

@app.callback(Output('h3im','children'),
             [Input('btimer', 'n_intervals')])
def display_hour3(n_intervals):
    h3urls = ["http://webcams.bsch.com.au/bondi_beach/1252x940.jpg?cache=%d" % random.randint(0,30000),
    "http://203.217.21.105:1050/jpg/1/image.jpg?cache=%d" % random.randint(0,30000),
    "http://192.168.1.108/snapshot.jpg",
    "http://192.168.1.107/snapshot.jpg"]
    print('Hour3 images updated',time.strftime('%H:%M:%S'),'n_intervals',n_intervals)
    t = generate_table(h3urls)
    return t

@app.callback(Output("h1im",'children'),
               [Input('ptimer', 'n_intervals')])
def display_hour(n_intervals):
    hurls = ["http://192.168.1.199/","http://192.168.1.200/"]
    print('Hour1 images updated',time.strftime('%H:%M:%S'),'n_intervals',n_intervals)
    t = generate_table(hurls)
    return t
    
if __name__ == '__main__':
    app.run_server(debug=True)
