# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

import dash

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.plotly as py
from plotly import graph_objs as go
import plotly.figure_factory as ff

from app import app 
from scripts import dvf_filter_and_compute as filter_and_compute
from scripts.values import dept_filter, ville_filter_unique
from scripts.values import df_dvf

###########################################################################
###########################################################################

layout = [

    # TOP CONTROLS : FILTERS - LINE 1
    html.Div(
        className="row",
        style={"marginBottom": "10"},
        children=[
            # FILTERS
            dept_filter,
            ville_filter_unique,

            # KPI - Moyenne prix ville
            html.Div(
                className="two columns",  # indicator",
                children=[
                    html.P(
                        "Prix moyen",
                        className="twelve columns indicator_text"
                    ),
                    html.P(
                        id="moyenne_prix_ville",
                        className="indicator_value"
                    ),
                ]
            ),

            # KPI - Moyenne surface ville
            html.Div(
                className="two columns",  # indicator",
                children=[
                    html.P(
                        "Surface moyenne",
                        className="twelve columns indicator_text"
                    ),
                    html.P(
                        id="moyenne_surface_ville",
                        className="indicator_value"
                    ),
                ],
            ),

            # KPI - Moyenne prix_m2 ville
            html.Div(
                className="two columns",  # indicator",
                children=[
                    html.P(
                        "Prix moyen au mètre carré",
                        className="twelve columns indicator_text"
                    ),
                    html.P(
                        id="moyenne_prix_m2_ville",
                        className="indicator_value"
                    ),
                ],
            ),
        ],
    ),
    html.Hr(),

    # GRAHPS : DISTRIBUTIONS - LINE 2
    html.Div(
        className='row',
        style={"marginTop": "5"},
        children=[
            html.Div(
                [
                    # GRAPH 1
                    html.Div(
                        [dcc.Graph(id='distribution_prix')],
                        className='four columns',
                        style={'margin-top': '10'}
                    ),
                    # GRAPH 2
                    html.Div(
                        [dcc.Graph(id='distribution_surface')],
                        className='four columns',
                        style={'margin-top': '10'}
                    ),
                    # GRAPH 3
                    html.Div(
                        [dcc.Graph(id='distribution_prix_m2')],
                        className='four columns',
                        style={'margin-top': '10'}
                    ),
                ]
            )
        ]
    ),
    html.Hr(),

    # GRAPHS : SCATTER PLOT - LINE 3
    html.Div(
        [
            # GRAPH 1
            html.Div(
                [dcc.Graph(id='scatter_prix_surface')],
                className='six columns',
                style={'margin-top': '2'}
            ),
            # GRAPH 2
            html.Div(
                [dcc.Graph(id='scatter_prix_m2_surface')],
                className='six columns',
                style={'margin-top': '2'}
            ),
        ],
        className="row",
        style={"marginTop": "2"},
    ),
    html.Hr(),

    # GRAPHS : SCATTER PLOT - LINE 4
    html.Div(
        className="row",
        style={"marginTop": "2"},
        children=[
            # GRAPH 1
            html.Div(
                [dcc.Graph(id='vente_par_mois')],
                className='four columns',
                style={'margin-top': '2'}
            ),
            # GRAPH 2
            html.Div(
                [dcc.Graph(id='prix_m2_surface_piece')],
                className='four columns',
                style={'margin-top': '2'}
            ),
            # GRAPH 3
            html.Div(
                [dcc.Graph(id='nb_piece_in_city')],
                className='four columns',
                style={'margin-top': '10'}
            ),
        ],
    ),
    html.Hr(),

    # GRAPHS : SCATTER PLOT - LINE 5
    html.Div(
        className="row",
        style={"marginTop": "2"},
        children=[
            # GRAPH 2
            html.Div(
                [dcc.Graph(id='plot_section')],
                className='twelve columns',
                style={'margin-top': '2'}
            ),
        ],
    ),
    html.Hr(),

]

###########################################################################
###########################################################################


def get_scatter_prix_m2_surface(df):
    trace1 = go.Scatter(
        x=df['surface'],
        y=df['prix_m2'],
        mode='markers',
        marker=dict(
            size=4,
            color=df['nb_piece'],
            colorscale='Viridis',
            showscale=True
        )
    )
    return {"data": [trace1]}


def get_scatter_prix_surface(df):
    trace1 = go.Scatter(
        x=df['surface'],
        y=df['prix'],
        mode='markers',
        marker=dict(
            size=4,
            color=df['prix_m2'],
            colorscale='Viridis',
            showscale=True
        )
    )
    return {"data": [trace1]}


def get_frequence(df):
    monthly = filter_and_compute.get_vente_par_periode(df, 'M')
    weekly = filter_and_compute.get_vente_par_periode(df, 'W')
    size = filter_and_compute.get_normalized_serie(monthly, 'mean') * 10
    print(size)
    trace1 = go.Scatter(
        x=monthly['date_mutation'],
        y=monthly['nunique'],
        mode='markers',
        name='Nombre de ventes par mois',
        marker=dict(size=size)
    )
    trace2 = go.Scatter(
        x=weekly['date_mutation'],
        y=weekly['nunique'],
        mode='lines+markers',
        name='Nombre de ventes par semaine'
    )
    data = [trace1, trace2]
    return {"data": data}


def get_plot_section(df):
    N = df.section.nunique()     # Number of boxes
    section_li = df.section.unique()
    section_li = [str(i) for i in section_li]
    section_li.sort()
    c = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, N)]

    data = [{
        'y': df[df['section'] == section_li[i]]['prix'],
        'type':'box',
        'marker':{'color': c[i]},
        'name':section_li[i]
    } for i in range(N)]

    layout = {'xaxis': {'showgrid': False, 'zeroline': False,
                        'tickangle': 60, 'showticklabels': False},
              'yaxis': {'zeroline': False, 'gridcolor': 'white'},
              'paper_bgcolor': 'rgb(233,233,233)',
              'plot_bgcolor': 'rgb(233,233,233)',
              }

    return {"data": data, 'layout': layout}


###########################################################################
###########################################################################


# INDICATEURS
@app.callback([Output('moyenne_prix_m2_ville', 'children'),
               Output('moyenne_prix_ville', 'children'),
               Output('moyenne_surface_ville', 'children'),
               Output('distribution_prix', 'figure'),
               Output('distribution_surface', 'figure'),
               Output('distribution_prix_m2', 'figure'),
               Output('prix_m2_surface_piece', 'figure'),
               Output('nb_piece_in_city', 'figure'),
               Output('vente_par_mois', 'figure'),
               Output('scatter_prix_m2_surface', 'figure'),
               Output('scatter_prix_surface', 'figure'),
               Output('plot_section', 'figure')],
              [Input('ville_dropdown', 'value')])
def moyenne_prix_m2_ville(ville, df=df_dvf):

    # Filtering
    dff = df[df['ville'] == ville]

    # INDICATORS
    moyenne_prix_m2 = filter_and_compute.calculate_mean_price_m2(dff)
    moyenne_surface = filter_and_compute.calculate_mean_surface(dff)
    moyenne_prix = filter_and_compute.calculate_mean_price(dff)

    # DISTRIBUTIONS
    # Distributions data
    dff_dist = dff[dff.prix < 500000]
    data_prix = [go.Histogram(x=dff_dist['prix'].values)]
    data_surface = [go.Histogram(x=dff_dist['surface'].values)]
    data_prix_m2 = [go.Histogram(x=dff_dist['prix_m2'].values)]

    # Distributions layout
    margin = go.layout.Margin(l=50, r=50, b=20, t=20, pad=4)
    layout = go.Layout(autosize=False, height=250, margin=margin)  # width=500,

    # Distribution calculations
    distrib_prix = {"data": data_prix, 'layout': layout}
    distrib_surface = {"data": data_surface, 'layout': layout}
    distrib_prix_m2 = {"data": data_prix_m2, 'layout': layout}

    # Prix au m2 par surface et nombre de pieces
    tmp = filter_and_compute.get_prix_m2_surface_piece(dff)
    data = [go.Bar(
        x=tmp[tmp.nb_piece == piece]['surface'],
        y=tmp[tmp.nb_piece == piece]['prix'],
        name=piece
    ) for piece in tmp.nb_piece.unique()]
    prix_m2_surface_piece = {"data": data}

    # Nombre d'appartement avec n pieces
    tmp = filter_and_compute.get_nb_piece_in_city(dff)
    trace1 = go.Bar(
        x=tmp['index'],
        y=tmp['nb_piece'],
        name='Nombre de pièces')
    data = [trace1]
    margin = go.layout.Margin(l=50, r=50, b=20, t=20, pad=4)
    layout = go.Layout(autosize=False,  height=250, margin=margin)  # width=500
    nb_piece_in_city = {"data": [trace1], 'layout': layout}

    # Fréquence des ventes
    frequence_vente = get_frequence(dff)

    # Scatter_plot
    scatter_prix_m2_surface = get_scatter_prix_m2_surface(dff)
    scatter_prix_surface = get_scatter_prix_surface(dff)

    # Boxplot sections
    sections_boxplot = get_plot_section(dff)

    # Computer response
    response = [moyenne_prix_m2, moyenne_prix, moyenne_surface,
                distrib_prix, distrib_surface, distrib_prix_m2,
                prix_m2_surface_piece, nb_piece_in_city,
                frequence_vente,
                scatter_prix_m2_surface, scatter_prix_surface,
                sections_boxplot]

    return response


