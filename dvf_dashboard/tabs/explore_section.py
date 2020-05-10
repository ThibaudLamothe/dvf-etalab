# -*- coding: utf-8 -*-
import json
import math

import pandas as pd
import flask
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
import numpy as np
from plotly import graph_objs as go

from app import app, indicator, millify, df_to_table
from scripts import filter_and_compute
from scripts.values import modele_color, dept_filter, ville_filter_unique, section_filter
from scripts.df_value import rep

df_dvf = rep['df_general']


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
    # html.Div(
    #     [   
    #         section_filter
    #     ],
    #     className="row",
    #     style={"marginBottom": "10"},
    #     ),


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
