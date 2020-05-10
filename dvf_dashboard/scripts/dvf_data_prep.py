# -*- coding: utf-8 -*-

# Making imports
import pandas as pd
import numpy as np
import datetime
import pickle


def load_dpt(dept_list, year_file='2018'):
    df_list = []
    FOLDER = '/Users/thibaudlamothe/Documents/Data/DVF/data_per_dept'
    for dept in dept_list:
        try:
            print(' - Loading dept {}'.format(dept))
            path = '{}/processed_{}/dept_{}.csv'.format(
                FOLDER, year_file, dept)
            df = pd.read_csv(path, low_memory=False)
            df_list.append(df)
        except:
            print(' - {} was not found.'.format(dept))
    df = pd.concat(df_list)
    return df


def compute_prix_m2(df):
    # print('> Computing m2...')
    df['prix_m2'] = df['prix'].div(df['surface']).apply(np.round)
    df = df[df['prix_m2'] < 10000]
    return df


def display_shape(df, msg='Shape'):
    print(' - {} : {} '.format(msg, df.shape))
    return df


def select_price_range(df, min_=0, max_=1000000):
    df_1 = df[df['prix'] > min_]
    df_2 = df_1[df_1['prix'] < max_]
    return df_2


def select_type(df, type_='Appartement'):
    df_1 = df[df['type_local'] == type_]
    df_1 = df_1.drop('type_local', axis=1)
    return df_1


def select_mutation(df, mutation='Vente'):
    df_1 = df[df['nature_mutation'] == mutation]
    df_1 = df_1.drop('nature_mutation', axis=1)
    return df_1


def transform_date(df):
    df['date_mutation'] = pd.to_datetime(df['date_mutation'], errors='coerce')
    return df


def select_cities(df, cities=None):
    if cities is None:
        return df

    df_list = []
    for city in cities:
        df_list.append(df[df['ville'] == city])
    df_final = pd.concat(df_list)
    return df_final


def calculate_adress(df, drop_col=False):
    df_1 = df.copy()
    df_1['adresse'] = df['no_voie'].apply(
        str) + ' ' + df['type_de_voie'] + ' ' + df['voie']
    if drop_col:
        df_1 = df_1.drop(['no_voie', 'type_de_voie', 'voie'], axis=1)
    return df_1


def preparingData(pick=False):

    print('PREPARING DATA')
    if not pick:
        print('on se traine')

        # PARAMETERS
        dpt_list = ['33', '35', '44', '51']
        rennes = ['RENNES', 'CESSON-SEVIGNE', 'CHANTEPIE']
        nantes = ['NANTES', 'REZE', 'ST SEBASTIEN SUR LOIRE', 'ST-HERBLAIN']
        bordeaux = ['BORDEAUX', 'TALENCE', 'PESSAC', 'MERIGNAC']
        autres = ['REIMS']  # + paris_list
        selected_cities = rennes + nantes + bordeaux + autres
        selected_col = ['date_mutation', 'prix_m2', 'surface', 
                        'surface_terrain',
                        'prix', 'ville', 'section', 'code_postal',
                        'nb_piece', 'dept', 'adresse']

        prix_min = 80000
        prix_max = 111000

        def select_price_range(df, prix_min, prix_max):
            df_new = df[df.prix < prix_min]
            df_new = df_new[df_new.prix > prix_max]
            return df_new

        # Loading raw data
        df = (load_dpt(dpt_list)
              .pipe(display_shape, 'Initial shape')
              .pipe(compute_prix_m2)
              .pipe(display_shape, 'Post m² shape')
              # .pipe(select_price_range, min_=prix_min, max_=prix_max)
              .pipe(display_shape, 'Post price shape')
              .pipe(select_cities, selected_cities)
              .pipe(select_type, 'Appartement')
              .pipe(select_mutation, 'Vente')
              .drop('code_voie', axis=1)
              .pipe(calculate_adress, drop_col=True)
              .pipe(display_shape, 'Final shape')
              .pipe(transform_date)
              .reset_index(drop=True)[selected_col]
              .set_index('date_mutation')
              .sort_index())

        print('RETURNING MODIFIED LOADED DATFRAMES')

        restitution = {'df_general': df,
                       }
        pickle.dump(restitution, open("../data/restitution.p", "wb"))
    else:
        print('on charge directement la restitution.')
        restitution = pickle.load(open("../data/restitution.p", "rb"))
    print('restitution ok')
    return restitution


#
if __name__ == "__main__":
    rep = preparingData(pick=True)
