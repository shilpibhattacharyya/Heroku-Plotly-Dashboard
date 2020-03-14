import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from collections import Counter
import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt
from matplotlib import colors as mcolors
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
from dash.dependencies import Input, Output
import operator
import functools
import plotly.express as px
from datetime import datetime, timedelta

def to_unix_time(dt):
    epoch =  datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Coronavirus Infections'
server = app.server



url_death="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"
url_recovered="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"

url="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"

df_death=pd.read_csv(url_death)
df_recov=pd.read_csv(url_recovered)
df=pd.read_csv(url)
#df = pd.read_csv('data/coronavirus.csv', index_col=False, header=0)
df.rename(columns = {'Province/State':'State', 'Country/Region':'Country'}, inplace = True)




countries_list=list(df.Country.unique())
d = {k:v for k,v in zip(countries_list,countries_list)}
result = [{"label": k, "value": v} for k,v in d.items()]

df_death.rename(columns = {'Province/State':'State', 'Country/Region':'Country'}, inplace = True)
df_recov.rename(columns = {'Province/State':'State', 'Country/Region':'Country'}, inplace = True)





cols_to_sum = [col for col in df.columns if '/20' in col] 
#d = datetime. datetime. today()

df['total_cases'] = df[datetime.strftime(datetime.now() - timedelta(days=1), '%-m/%-d/%y')]
# df_death=df_death.sort_values(by=['total_cases'])
# df_recov=df_recov.sort_values(by=['total_cases'])
df.sort_values(by=['total_cases'],ascending=False, inplace=True)

df_25=df[:100]
#df['total_cases'] = df[cols_to_sum].sum(axis=1)  # assigned to a column

scl = [0,"rgb(150,0,90)"],[0.125,"rgb(0, 0, 200)"],[0.25,"rgb(0, 25, 255)"],\
[0.375,"rgb(0, 152, 255)"],[0.5,"rgb(44, 255, 150)"],[0.625,"rgb(151, 255, 0)"],\
[0.75,"rgb(255, 234, 0)"],[0.875,"rgb(255, 111, 0)"],[1,"rgb(255, 0, 0)"]



x = pd.date_range(start = "2020-01-22", end = datetime.now(), freq = "D")
x = [pd.to_datetime(date, format='%Y-%m-%d').date() for date in x]

y_index = pd.date_range(start = datetime.strftime(datetime(2020, 1, 22),'%-m/%-d/%y'), end = datetime.strftime(datetime.now()- timedelta(1),'%-m/%-d/%y'), freq = "D")
y_index = [datetime.strftime(date,'%-m/%-d/%y') for date in y_index]




# Create a Dash layout
app.layout = html.Div(children=[
    html.H1('Live Coronovirus Infections Globally'),

    html.Div('''
        A Visualization of Infections from 01/22/2020 till Today
        '''),
       dcc.Dropdown(
        id='demo-dropdown',
        options=result,
        value=['US'],
        multi=True
        
    ),
    dcc.Checklist(id='select-all',
                  options=[{'label': 'Select All', 'value': 1}], value=result),
    html.Div(id='tabs-content-example')

 ])

@app.callback(
Output('tabs-content-example', 'children'),
[Input('demo-dropdown', 'value')])
    
def update_output(value):
    return html.Div(children=[html.Div([html.Div(dcc.Graph(
        id='example-map',
        
        figure= go.Figure(data=go.Scattergeo(
        locationmode = 'country names',
        lon = df.loc[df['Country'].isin(value)]['Long'],
        lat = df.loc[df['Country'].isin(value)]['Lat'],
        text = df.loc[df['Country'].isin(value)]['State'].astype(str),
        mode = 'markers',
        marker = dict(
            size = 8,
            opacity = 0.8,
            reversescale = True,
            autocolorscale = False,
            symbol = 'square',
            line = dict(
                width=1,
                color='rgba(102, 102, 102)'
            ),
            colorscale = 'Bluered',#'Blues',
            cmin = 0,
            color = df.loc[df['Country'].isin(value)]['total_cases'],
            cmax = df.loc[df['Country'].isin(value)]['total_cases'].max(),
            colorbar_title="Total Infected Cases"
        )),layout=dict(height=800, width=1600, title="Total Infected Cases of Corona Virus from 01/22/2020 till Today in the Selected Country(ies)")))),

    # html.Br(),
    # html.Div(children='''
    # '''),
    html.Div(
    dcc.Graph(
        id='example-scatter',

        figure=go.Figure(data = [go.Scatter(
        x=x,
        y=[df.loc[df['Country'].isin(value)].sum()[str(d)] for d in y_index],
        mode='lines+markers',
        name='Confirmed Cases',
        marker_color='rgba(152, 0, 0, .8)'),go.Scatter(
        x=x,
        y=[df_death.loc[df['Country'].isin(value)].sum()[str(d)] for d in y_index],
        name='Deaths Caused',
        mode='lines+markers',
        marker_color='rgb(231, 99, 250)'),
        go.Scatter(
        x=x,
        y=[df_recov.loc[df_recov['Country'].isin(value)].sum()[str(d)] for d in y_index],
        name='Recovered Cases',
        mode='lines+markers',
        marker_color='rgb(17, 157, 255)')],

        layout = go.Layout(title="Trend of Infected Cases of Corona Virus from 01/22/2020 till Today in the Selected Country(ies)",height=600,xaxis = dict(
                   range = [to_unix_time(datetime(2020, 1, 21)),
                            to_unix_time(datetime.now())]
                            )
    ))))]),
    

    html.Br(),
    html.Br(),


    html.Div(children='''
    '''),

        dcc.Graph(
        id='example-graph1',
        
        figure=go.Figure(data=[go.Bar(
            x=df_25.loc[df_25['Country'].isin(value)]['State'].tolist(), y=df_25.loc[df_25['Country'].isin(value)]['total_cases'].tolist(),
            text=df_25.loc[df_25['Country'].isin(value)]['total_cases'].tolist(),
            textposition='auto',
            #layout=go.Layout(barmode='group',title="Coronavirus Infection across Mainland China")
            #title='Coronavirus Infection across Mainland China'
        )],layout=go.Layout(height=600,title="Coronavirus Infections across the Selected Country(ies)",
        xaxis=dict(
        tickangle= 35,
        showticklabels=True,
        type='category',
        tickmode='linear')))

    ),

    html.Br(),
    html.Br(),

    html.Div(children='''
    '''),

    
        dcc.Graph(
                id='example-graph3',
                figure={
                    'data': [                          
                        go.Pie(                                        
                            labels=list(df_25.loc[df_25['Country'].isin(value)]['State']),
                            values=list(df_25.loc[df_25['Country'].isin(value)]['total_cases']),  
                            hoverinfo='label+value+percent'                                     
                            )                              
                        ],
                    'layout':{
                            'showlegend':True,
                            'title':'All Infected States in the Selected Country(ies)',
                            'height':800, 
                            'width':1500
                            
                    }  
                }
            )
])


    
    if __name__ == '__main__':
        app.run_server(debug=True)

