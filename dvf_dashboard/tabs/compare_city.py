# -*- coding: utf-8 -*-
import json
import math
import numpy as np
import pandas as pd

import flask
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
from plotly import graph_objs as go


from app import app, indicator, millify, df_to_table
from scripts.values import modele_color, dept_filter, ville_filter_multi
from scripts.df_value import rep
from scripts import filter_and_compute

df_dvf = rep['df_general']


##############################################################################
##############################################################################

layout = [


    # TOP CONTROLS : FILTERS - LINE 1
    html.Div(
        [
            dept_filter,
            ville_filter_multi,
        ],
        className="row",
        style={"marginBottom": "10"},
    ),

    html.Div(
        [
            # GRAPH 1
            html.Div(
                [
                    dcc.Graph(id='comp_city_price')
                ],
                className='six columns',
                style={'margin-top': '10'}
            ),

        ],
        className="row",
        style={"marginTop": "5"},
    ),

]

##############################################################################
##############################################################################


# GRAPH : COUT REVIENT PAR VEHICULE
@app.callback(Output('comp_city_price', 'figure'),
              [Input('ville_dropdown_multi', 'value')
               ])
def comp_city_price(ville, df=df_dvf):
    print(ville)
    print(df.shape)
    df = df[df['ville'].isin(ville)]
    print(df.shape)
    data = [
        go.Scatter(
            x=df[df['ville'] == i]['surface'],
            y=df[df['ville'] == i]['prix'],
            text=df[df['ville'] == i]['prix_m2'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ) for i in df.ville.unique()
    ]

    layout = go.Layout(
        xaxis={'type': 'log', 'title': 'GDP Per Capita'},
        yaxis={'title': 'Life Expectancy'},
        margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
        legend={'x': 0, 'y': 1},
        hovermode='closest'
    )
    return {"data": data}  # , 'layout':layout}
