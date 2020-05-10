
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from app import app


import pickle
import pandas as pd
import numpy as np
from scripts import dvf_data_prep

# PATH FOR INDEX
urls = {
    "css_style_url" : 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css',
    "favicon_url" : 'https://www.google.com/favicon.ico',
    "img_top_url" : 'https://fr.wikipedia.org/wiki/Le_Bon_Coin#/media/File:Leboncoin.fr_Logo.PNG',
    "font_url" : 'https://use.fontawesome.com/releases/v5.2.0/css/all.css',
    "stylesheet_url" : 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css',
    "google_api_url" : 'https://fonts.googleapis.com/css?family=Dosis',
    "font_google_url" : 'https://fonts.googleapis.com/css?family=Open+Sans',
    "font_google_url_2" : 'https://fonts.googleapis.com/css?family=Ubuntu',
    "dash_css_url" : 'https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw/cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css'
}

# LOADING DATASETS
# df_dvf = pd.read_csv('/Users/thibaudlamothe/OneDrive - Capgemini/Documents/Data/DVF/data_per_dept/processed_2018/dept_35.csv')
# df_immo = pickle.load(open('C:/Users/Thibaud Lamothe/Documents/Python/10_lbc_scrap/02_analysis/df.p', 'rb'))
# df_new = pickle.load(open('C:/Users/Thibaud Lamothe/Documents/Python/10_lbc_scrap/02_analysis/df_new.p', 'rb'))
# df_old = pickle.load(open('C:/Users/Thibaud Lamothe/Documents/Python/10_lbc_scrap/02_analysis/df_old.p', 'rb'))

# LOADING DATA FOR APP
rep = dvf_data_prep.preparingData(pick=True)
df_dvf = rep['df_general']



dept_conv = {33: '33 - Gironde',
             35: '35 - Ille et Vilaine',
             44: '44 - Loire-Atlantiqie',
             51: '51 - Marne'}

ville_dict = [{"label": i, "value": i} for i in df_dvf['ville'].unique()]
dept_dict = [{"label": dept_conv[i], "value":i} for i in df_dvf['dept'].unique()]
section_dict = [{"label": i, "value": i} for i in df_dvf['section'].unique()[:40]]


####################################################################################################
####################################################################################################
####################################################################################################


@app.callback(
    Output('ville_dropdown', 'options'),
    [Input('dept_dropdown', 'values')])
def set_cities_options(selected_country, df=df_dvf):
    print(selected_country)
    # city_to_dis = df[df['dept'].isin(selected_country)]['ville'].unique()
    # city_to_dis = df[df['dept'] == selected_country]['ville'].unique()
    city_to_dis = ['BORDEAUX', 'NANTES', 'ST-HERBLAIN', 'TALENCE', 'MERIGNAC', 'RENNES', 'REIMS', 'REZE', 'PESSAC', 'ST SEBASTIEN SUR LOIRE', 'CHANTEPIE', 'CESSON-SEVIGNE']
    return [{"label": i, "value": i} for i in city_to_dis] 


####################################################################################################
####################################################################################################
####################################################################################################


# Filtre departement
dept_filter = html.Div(
    [
        html.P('Departement'),
        dcc.Checklist(
            id='dept_dropdown',
            options=dept_dict,
            labelStyle = {'display': 'block', 'cursor': 'pointer', 'margin-left':'20px'},
            #values= [i['value']for i in dept_dict],
        ),
    ],
    className="two columns",
)

# Filtre ville selection unique
ville_filter_unique = html.Div(
    [
        html.P('Ville'),
        dcc.Dropdown(
            id='ville_dropdown',
            options=ville_dict,
            multi=False,
            value='BORDEAUX',
            # value=[i['value']for i in ville_dict],
        ),
    ],
    className="two columns",
)

# Filtre ville selection multiple
ville_filter_multi = html.Div(
    [
        html.P('Ville'),
        dcc.Dropdown(
            id='ville_dropdown_multi',
            options=ville_dict,
            value=[i['value']for i in ville_dict],
            multi=True
        ),
    ],
    className="eight columns",
)

# Filtre section
section_filter = html.Div(
    [
        html.P('Section'),
        dcc.Dropdown(
            id="section_dropdown",
            options=section_dict,
            multi=True,
            value=[i['value'] for i in section_dict],
            disabled=True,
        )
    ],
    className="eight columns",
)


# Ensemble de filtre
filter_1 = html.Div(
    [
        dept_filter,
        ville_filter_unique,
        section_filter
    ],
    className="row",
    style={"marginBottom": "10"},
)


# Réinitialisation de filtres
filter_2 = dcc.RadioItems(
    id='finition_selector',
    options=[
        {'label': 'Tous les filtres ', 'value': 'all'},
        {'label': 'Selection ', 'value': 'custom'}
    ],
    value='all',
    labelStyle={'display': 'inline-block'}
)

