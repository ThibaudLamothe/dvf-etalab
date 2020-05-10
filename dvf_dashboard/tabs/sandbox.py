# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.plotly as py
from plotly import graph_objs as go

from app import app
from scripts.values import filter_1, filter_2 
from scripts.values import df_dvf

############################################################################################################################################
############################################################################################################################################
############################################################################################################################################

layout = [


    # TOP CONTROLS : FILTERS - LINE 1
    filter_1,
    filter_2,
    html.Div(
        [
            # GRAPH 1
            html.Div(
                [
                    dcc.Graph(id='dvf_sand')
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
@app.callback(Output('dvf_sand', 'figure'),
              [Input('dept_dropdown', 'value')
               ])

def dvf_sand(model, df=df_dvf):
    print(model)
    print(df.columns)
    print(df.head())
    df = df[df['dept'].isin(model)]
    granularity ='dept'
    print(df.head())

    i = 51
    d = [df[df[granularity] == i]['surface'],
            df[df[granularity] == i]['prix']]
        
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
            name=str(i)
        ) for i in df[granularity].unique()
    ]

    return {"data": data}