# -*- coding: utf-8 -*-
import dash
import time
import random
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import urllib.request
import base64


# image_url = "http://webcams.bsch.com.au/bondi_beach/1252x940.jpg?cache=%d" % random.randint(0,30000)
# local_filename, headers = urllib.request.urlretrieve(image_url)
# encoded_image = base64.b64encode(open(local_filename, 'rb').read())

refresh_image = 1200 # secs

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[

    dcc.Interval(
            id='ptimer',
            interval=refresh_image*1000 ,
            disabled=False,
            n_intervals=0
            ),


    html.H1(children='Test'),
    
    html.Div( children=[
        html.Img( id="bbeach", #n_clicks=0,
            width=500,height=400,
            src = "http://webcams.bsch.com.au/bondi_beach/1252x940.jpg?cache=%d" % random.randint(0,30000))
            ], style = {'display': 'block'})
            
        # html.Div(id='modal', children=[
            # html.Img(
                # src="http://webcams.bsch.com.au/bondi_beach/1252x940.jpg?cache=%f" % time.time(),
                # height='640',
                # width='470',
                # style={
                    # 'display':'block',
                    # 'margin-left': 'auto',
                    # 'margin-right': 'auto'
                # })
           # ], style={'display': 'none'}),

       
])

@app.callback(Output('bbeach','src'),
              [Input('ptimer', 'n_intervals')])
def display_image(n_intervals):
    sauce = "http://webcams.bsch.com.au/bondi_beach/1252x940.jpg?cache=%d" % random.randint(0,30000)
    print(time.strftime('%H:%M:%S'),'n_intervals',n_intervals,sauce)
    return sauce
    # lastup = time.time()
    # image_url = "http://webcams.bsch.com.au/bondi_beach/1252x940.jpg?cache=%f" % lastup
    # local_filename, headers = urllib.request.urlretrieve(image_url)
    # encoded_image = base64.b64encode(open(local_filename, 'rb').read())
    # print('n_intervals',n_intervals,image_url)
    # return encoded_image

if __name__ == '__main__':
    app.run_server(debug=True)
