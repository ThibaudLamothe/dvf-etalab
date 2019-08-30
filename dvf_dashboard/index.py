# -*- coding: utf-8 -*-
import flask
import pandas as pd
import math

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
from plotly import graph_objs as go

from app import app, server
from apps import compare_city, explore_city, explore_section
from apps import dvf_maps, dvf_sandbox
import dvf_functions as ldf

# Necessary url definition
css_style_url = 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'
favicon_url = 'https://www.google.com/favicon.ico'
img_top_url = 'https://fr.wikipedia.org/wiki/Le_Bon_Coin#/media/File:Leboncoin.fr_Logo.PNG'
font_url = 'https://use.fontawesome.com/releases/v5.2.0/css/all.css'
stylesheet_url = 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'
google_api_url = 'https://fonts.googleapis.com/css?family=Dosis'
font_google_url = 'https://fonts.googleapis.com/css?family=Open+Sans'
font_google_url_2 = 'https://fonts.googleapis.com/css?family=Ubuntu'
dash_css_url = 'https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw/cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css'


# Adding information about app
app.css.append_css({'external_url': css_style_url})  # noqa: E501
app.title = 'DVF - Exploration'

app.head = [
    html.Link(
        href=favicon_url,
        rel='icon'
    ),
]
app.layout = html.Div(
    [
        # header
        html.Div([

            html.Span("DVF Analysis", className='app-title'),

            html.Div(
                html.Img(src=img_top_url, height="100%"),
                style={"float": "right", "height": "100%"})
        ],
            className="row header"
        ),


        # tabs
        html.Div([

            dcc.Tabs(
                id="tabs",
                style={"height": "20", "verticalAlign": "middle"},
                children=[
                    dcc.Tab(id="compare_city",
                            label="Comparaison  villes", value="compare_city"),
                    dcc.Tab(id="explore_city",
                            label="Exploration ville", value="explore_city"),
                    dcc.Tab(id="explore_section",
                            label="Exploration section",
                            value="explore_section"),
                    dcc.Tab(id="dvf_maps", label="Cartographie",
                            value="dvf_maps"),
                    dcc.Tab(id="dvf_sandbox", label="Bac à sable",
                            value="dvf_sandbox"),
                ],
                value="general_tab",
            )

        ],
            # className="row ta
        ),


        # Tab content
        html.Div(id="tab_content", className="row", style={"margin": "2% 3%"}),

        html.Link(href=font_url, rel="stylesheet"),
        html.Link(href=stylesheet_url, rel="stylesheet"),
        html.Link(href=google_api_url, rel="stylesheet"),
        html.Link(href=font_google_url, rel="stylesheet"),
        html.Link(href=font_google_url_2, rel="stylesheet"),
        html.Link(href=dash_css_url, rel="stylesheet")
    ],
    className="row",
    style={"margin": "0%"},
)


@app.callback(Output("tab_content", "children"), [Input("tabs", "value")])
def render_content(tab):
    if tab == "compare_city":
        return compare_city.layout
    if tab == "explore_city":
        return explore_city.layout
    if tab == "explore_section":
        return explore_section.layout
    if tab == "dvf_maps":
        return dvf_maps.layout
    if tab == "dvf_sandbox":
        return dvf_sandbox.layout
    # elif tab == "gestion":
    #     return gestion_parc.layout
    else:
        return compare_city.layout


if __name__ == "__main__":
    app.run_server(debug=True)
    import df_value as dfv
