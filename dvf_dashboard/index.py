# -*- coding: utf-8 -*-
import flask
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from app import app, server
from tabs import compare_city, explore_city
from tabs import explore_section, maps
from tabs import sandbox

from scripts.values import urls

# Adding information about app
app.css.append_css({'external_url': urls["css_style_url"]})  # noqa: E501
app.title = 'DVF - Exploration'
app.head = [html.Link( href=urls["favicon_url"], rel='icon')]


# Layout
app.layout = html.Div(
    className="row",
    style={"margin": "0%"},
    children=[

        # Header
        html.Div(
            className="row header",
            children=[
                html.Span("DVF Analysis", className='app-title'),
                html.Div(html.Img(src=urls["img_top_url"], height="100%"), style={"float": "right", "height": "100%"})
            ],
        ),

        # Tabs
        html.Div(
            [
                dcc.Tabs(
                    id="tabs",
                    style={"height": "20", "verticalAlign": "middle"},
                    value="general_tab",
                    children=[
                        dcc.Tab(id="compare_city", label="Comparaison  villes", value="compare_city"),
                        dcc.Tab(id="explore_city", label="Exploration ville", value="explore_city"),
                        dcc.Tab(id="explore_section", label="Exploration section", value="explore_section"),
                        dcc.Tab(id="dvf_maps", label="Cartographie", value="dvf_maps"),
                        dcc.Tab(id="dvf_sandbox", label="Bac à sable", value="dvf_sandbox"),
                    ],
                    
                )
            ],
        ),

        # Tab content
        html.Div(id="tab_content", className="row", style={"margin": "2% 3%"}),

        # Urls loading
        html.Link(href=urls["font_url"], rel="stylesheet"),
        html.Link(href=urls["stylesheet_url"], rel="stylesheet"),
        html.Link(href=urls["google_api_url"], rel="stylesheet"),
        html.Link(href=urls["font_google_url"], rel="stylesheet"),
        html.Link(href=urls["font_google_url_2"], rel="stylesheet"),
        html.Link(href=urls["dash_css_url"], rel="stylesheet")

    ],
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
    else:
        return compare_city.layout


if __name__ == "__main__":
    app.run_server(debug=True)
