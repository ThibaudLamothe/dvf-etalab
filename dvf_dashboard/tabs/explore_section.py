# -*- coding: utf-8 -*-
import json
import math
import numpy as np
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.plotly as py
from plotly import graph_objs as go

from app import app
from scripts.values import dept_filter, ville_filter_unique, section_filter
from scripts.values import df_dvf


############################################################################################################################################
############################################################################################################################################
############################################################################################################################################

layout = [

    html.Div(
        [   
            dept_filter,
            ville_filter_unique,
            section_filter
        ],
        className="row",
        style={"marginBottom": "10"},
        ),

    html.Div(
        [
            # GRAPH 1
            html.Div(
                [
                    dcc.Graph(id='explo_sec')
                ],
                className='six columns',
                style={'margin-top': '10'}
            ),

        ],
        className="row",
        style={"marginTop": "5"},
    ),

]

############################################################################################################################################
############################################################################################################################################
############################################################################################################################################


# GRAPH : COUT REVIENT PAR VEHICULE
@app.callback(Output('explo_sec', 'figure'),
              [Input('model_dropdown', 'value')
               ])
def explo_sec(model, df=df_dvf):
    
    df = df[df['dept'].isin(model)]
    granularity ='dept'
    data = [
        go.Scatter(
            x=df[df[granularity] == i]['surface'],
            y=df[df[granularity] == i]['prix'],
            text=df[df[granularity] == i]['code_postal'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ) for i in df.ville.unique()
    ]

    return {"data": data}
