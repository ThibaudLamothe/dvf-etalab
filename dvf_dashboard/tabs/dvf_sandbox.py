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
from scripts.values import modele_color, filter_1, filter_2 #, test_d
from scripts.df_value import rep

df_dvf = rep['df_general']


############################################################################################################################################
############################################################################################################################################
############################################################################################################################################


# indicateur_total = html.Div(
#     # className="two columns indicator",
#     className='three columns',
#     children=[
#         html.P(
#             "Prix moyen",
#             className="twelve columns indicator_text"
#         ),
#         html.P(
#             id="moyenne_prix_ville",
#             className="indicator_value"
#         ),

#         html.P(
#             "Surface moyenne",
#             className="twelve columns indicator_text"
#         ),
#         html.P(
#             id="moyenne_surface_ville",
#             className="indicator_value"
#         ),
#         html.P(
#             "Prix moyen au mètre carré",
#             className="twelve columns indicator_text"
#         ),
#         html.P(
#             id="moyenne_prix_m2_ville",
#             className="indicator_value"
#         ),
#     ],
# )   


layout = [


    # TOP CONTROLS : FILTERS - LINE 1
    filter_1,
    filter_2,
   # test_d,
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
        
    print(df.info())
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




# # INDICATEUR : NB VEHICULES
# @app.callback(Output('ville_filtered', 'children'),
#               [Input('ville_dropdown', 'value')])
# def filter_ville(ville, df=df_dvf):
#     print('LA')
#     print('VILLE', ville)
#     print(df.shape)
#     dff = df[df['ville'] == ville]
#     print(dff.shape)
#     return dff.to_json()


# # INDICATEUR : NB VEHICULES
# @app.callback(Output('moyenne_prix_m2_ville', 'children'),
#               [Input('ville_filtered', 'children')])
# def moyenne_prix_m2_ville(df):
#     df = pd.read_json(df)
#     moyenne_prix_m2 = df['prix_m2'].mean()
#     moyenne_prix_m2 = str(np.round(moyenne_prix_m2, 2)) + ''
#     return moyenne_prix_m2




# @app.callback(Output('distribution_prix_dist', 'figure'),
#               [Input('ville_dropdown', 'value')
#                ])
# def distribution_prix_dist(model, df=df_dvf):
#     dff = df[df['ville'].isin(model)]
#     dff = dff[dff.prix < 500000]

#     # Add histogram data
#     x1 =dff['prix'].values

#     # Group data together
#     hist_data = [x1] #, x2, x3, x4]
#     group_labels = ['Distribution du prix']

#     # Create distplot with custom bin_size
#     fig = ff.create_distplot(hist_data, group_labels, bin_size=100)
#     return fig
