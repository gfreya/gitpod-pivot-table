import dash
from dash import dash_table
from dash import dcc # dash core components
from dash import html
import dash_pivottable
import numpy as np

import pandas as pd

df = pd.read_csv('https://bit.ly/elements-periodic-table')

index_options = df.columns
column_options = df.columns
value_options = df.columns

agg_options = {'min':np.min, 'max':np.max, 'identity':lambda x:x, 'mean':np.mean}

app = dash.Dash(__name__)

app.layout = html.Div([
    
    html.H2("Index"),
    html.Div(
        [
            dcc.Dropdown(
                id="Index",
                options=[{
                    'label': i,
                    'value': i
                } for i in index_options],
                value='All Indices'),
        ],
       ),
    html.H2("Column"),
    html.Div(
        [
            dcc.Dropdown(
                id="Column",
                options=[{
                    'label': i,
                    'value': i
                } for i in column_options],
                value='All Columns'),
        ],
       ),
    html.H2("Value"),
    html.Div(
        [
            dcc.Dropdown(
                id="Value",
                options=[{
                    'label': i,
                    'value': i
                } for i in value_options],
                value='All Values'),
        ],
       ),
    html.H2("Aggfunc"),
    html.Div(
        [
            dcc.Dropdown(
                id="Aggfunc",
                options=[{
                    'label': i,
                    'value': i
                } for i in agg_options.keys()],
                value='All Functions'),
        ],
       ),
    dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
)
])


@app.callback(
    [dash.dependencies.Output("table", "data"),
    dash.dependencies.Output("table", "columns")],
    [dash.dependencies.Input('Index', 'value'),
     dash.dependencies.Input('Column', 'value'),
     dash.dependencies.Input('Value', 'value'),
     dash.dependencies.Input('Aggfunc', 'value')
     ])

def update_table(Index, Column, Value, Aggfunc):
    if Index == "All Indices" or Column == "All Columns" or Value == "All Values" or Aggfunc=="All Functions":
        df_updated = df.copy()
    else:
        


        df_updated = df.pivot_table(
            index=Index,
            columns=Column, 
            values=Value,
            aggfunc=agg_options[Aggfunc],
            fill_value=0)

    columns=[{"name": str(i), "id": str(i)} for i in df_updated.columns]
    data=df_updated.to_dict('records')
    return [data,columns]
    
    

    

app.run_server(debug=True, host="0.0.0.0")