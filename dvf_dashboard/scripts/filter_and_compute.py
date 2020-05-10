import numpy as np
import pandas as pd
import datetime
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






################################################################################################
################################################################################################
################################################################################################


def filterVehicle(df, voiture_name, origine, serigraphie,
                  energie=None, genre=None, marque_type=None, categorie_pn=None, article=None,
                  start_date=None, end_date=None, dept=None):
    df = df[df['VOITURE_NAME'].isin(voiture_name)]
    df = df[df['ORIGINE'].isin(origine)]
    df = df[df['SERIGRAPHIE'].isin(serigraphie)]
    if dept:
        df = df[df['DEPT_ACTUEL'].isin(dept)]
    return df


def getPctDispo(df_car, df_maint):
    nb_dispo = getParcVolume(df_car)['nombre_vehicule']
    nb_maint = getVehiculeEnMaintenance(df_maint)['nb_vehicule_maintenu']
    pct_parc_dispo = np.round((1 - nb_maint / nb_dispo) * 100, 2)
    return {'pct_parc_dispo': pct_parc_dispo}


def getCoutKM(df):
    cout_moyen_km = df['TOTAL'].sum() / df['KM'].sum()
    cout_moyen_km = np.round(cout_moyen_km, 2)
    return {'cout_moyen_km': cout_moyen_km}


def getFrequentIntervention(df, top=10):  # df_maintenance_small
    #most_frequent_intervention =  df.ARTICLE.value_counts()[:top]
    most_frequent_intervention = df.NATURE.value_counts()[:top]
    most_frequent_intervention = most_frequent_intervention.to_dict()
    return most_frequent_intervention

# nb passage atelier


def getNombreVehiculeAccidente(df):  # df_accident
    nb_vehicule_accidente = df.ID.nunique()
    return {'nb_vehicule_accidente': nb_vehicule_accidente}


def getNombreAccident(df):  # df_accident
    nb_accident = df.NUMERO_SINISTRE_CONTENTIEUX.nunique()
    return {'nb_accident': nb_accident}
