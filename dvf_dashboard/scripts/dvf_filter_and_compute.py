import datetime
import numpy as np
import pandas as pd
from collections import Counter


def calculate_mean_price(df):
    moyenne_prix = df['prix'].mean()
    moyenne_prix = int(moyenne_prix)
    moyenne_prix = str(moyenne_prix)[:-3] + ' ' + str(moyenne_prix)[-3:] + '€'
    return moyenne_prix


def calculate_mean_price_m2(df):
    moyenne_prix_m2 = df['prix_m2'].mean()
    moyenne_prix_m2 = str(np.round(moyenne_prix_m2, 2)) + ''
    return moyenne_prix_m2


def calculate_mean_surface(df):
    moyenne_surface = df['surface'].mean()
    moyenne_surface = np.round(moyenne_surface, 2)
    return moyenne_surface


def get_vente_par_periode(df, period):
    tmp = df.resample(period).agg({'prix_m2': ['nunique', 'mean']}).apply(
        np.round).droplevel(level=0, axis=1).reset_index()
    tmp['date_mutation'] = tmp['date_mutation'].apply(
        str).apply(lambda x: x[:10])
    return tmp


def get_normalized_serie(df, col):
    normalized = ((df[col] - df[col].min()) / (df[col].max()-df[col].min())+1)
    return normalized


def get_prix_m2_surface_piece(df):
    tmp = df.groupby(['surface', 'nb_piece']).mean()[
        ["prix_m2", 'prix']].apply(np.round).reset_index().iloc[:45]
    return tmp


def get_nb_piece_in_city(df):
    tmp = df[df['nb_piece'] < 10]
    tmp = pd.DataFrame(
        tmp['nb_piece'].value_counts().sort_index().reset_index())
    return tmp






