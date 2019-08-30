import numpy as np
from df_value import rep

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from app import app


df_dvf = rep['df_general']

dept_conv = {33: '33 - Gironde',
             35: '35 - Ille et Vilaine',
             44: '44 - Loire-Atlantiqie',
             51: '51 - Marne'}

ville_dict = [{"label": i, "value": i} for i in df_dvf['ville'].unique()]
dept_dict = [{"label": dept_conv[i], "value":i}
             for i in df_dvf['dept'].unique()]
section_dict = [{"label": i, "value": i}
                for i in df_dvf['section'].unique()[:40]]


####################################################################################################
####################################################################################################
####################################################################################################


@app.callback(
    Output('ville_dropdown', 'options'),
    [Input('dept_dropdown', 'values')])
def set_cities_options(selected_country, df=df_dvf):
    print(selected_country)
    #city_to_dis = df[df['dept'].isin(selected_country)]['ville'].unique()
    city_to_dis = ['BORDEAUX', 'NANTES', 'ST-HERBLAIN', 'TALENCE', 'MERIGNAC', 'RENNES', 'REIMS', 'REZE', 'PESSAC', 'ST SEBASTIEN SUR LOIRE', 'CHANTEPIE', 'CESSON-SEVIGNE']
    # city_to_dis = df[df['dept'] == selected_country]['ville'].unique()
    print(city_to_dis)
    #val = [{"label": i, "value": i} for i in city_to_dis]
    val = [{"label": i, "value": i} for i in city_to_dis]
    print(val)
    return val 



####################################################################################################
####################################################################################################
####################################################################################################



dept_filter = html.Div(
            [
                html.P('Departement'),

                # dcc.Dropdown(
                #             id='dept_dropdown',
                #             options=dept_dict,
                #             value= [i['value']for i in dept_dict],
                #             multi=True
                #         ),
                dcc.Checklist(
                            id='dept_dropdown',
                            options=dept_dict,
                            #values= [i['value']for i in dept_dict],
                            labelStyle = {'display': 'block', 'cursor': 'pointer', 'margin-left':'20px'}
                            
                        ),
            ],
            className="two columns",
        )


ville_filter_unique = html.Div(
            [
                html.P('Ville'),

                dcc.Dropdown(
                    id='ville_dropdown',
                    options=ville_dict,
                    # value=[i['value']for i in ville_dict],
                    value='BORDEAUX',
                    multi=False
                ),
            ],
            className="two columns",
        )

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

filter_1 = html.Div(
    [   dept_filter,
        ville_filter_unique,
        section_filter
    ],
    className="row",
    style={"marginBottom": "10"},
)


filter_2 = dcc.RadioItems(
    id='finition_selector',
    options=[
        {'label': 'Tous les filtres ', 'value': 'all'},
        {'label': 'Selection ', 'value': 'custom'}
    ],
    value='all',
    labelStyle={'display': 'inline-block'}
)


####################################################################################################
####################################################################################################
####################################################################################################


dict_voiture_name = {'partner': 'Partner',
                     'expert': 'Expert',
                     'visco': 'Visco',
                     'clio': 'Clio',
                     'berlingo': 'Berlingo',
                     'mondeo': 'Mondeo'}

dict_origine = {'gendarmerie': 'Gendarmerie Nationale',
                'police': 'Police Nationale'}

year_colors = {
    '2015-01-01 00:00:00': "#007aea",
    '2016-01-01 00:00:00': "#004ac7",
    '2017-01-01 00:00:00': "#000cae",
    '2018-01-01 00:00:00': "#002065",
}

origine_color = {'police': '#007aea',
                 'gendarmerie': '#000cae'}

modele_color = {'partner': '#003f8c',
                'expert': '#8c3d96',
                'visco': '#dc3b7c',
                'clio': '#ff644d',
                'berlingo': '#ffa600',
                'mondeo': '#dc3b7c'}


# maintenance_color = {'Préventif': '#003f8c',
#                      'Curatif': '#8c3d96',
#                      'Pneumatique': '#dc3b7c',
#                      'Accident': '#ff644d',
#                      'Remise en état': '#ffa600',
#                      'Dépannage': '#dc3b7c'}
