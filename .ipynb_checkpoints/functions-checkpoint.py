import string

def transfoCol(ancien, ponctuation=None, accent=None, replacer='_'):
    """Description : simplifie une chaine de caractère en supprimant les majuscules, la ponctuation, les accents et les espaces
    inputs :
        - ancien as string : chaine à modifier
        - ponctuation as list : liste des caractères à retirer
        - accent as dict : dictionnaire des caractères à modifier par un autre
    outputs:
        - string : chaine de caractère modifiée (simplifiée)
    """  
    
    if not ponctuation:
        caracters_to_remove = list(string.punctuation) + [' ','°']
        ponctuation = {initial:replacer for initial in caracters_to_remove}

    if not accent:
        avec_accent = ['é', 'è', 'ê', 'à', 'ù', 'ç', 'ô', 'î', 'â']
        sans_accent = ['e', 'e', 'e', 'a', 'u', 'c', 'o', 'i', 'a']
        accent = {sans:avec for sans, avec in zip(avec_accent, sans_accent)}
    
    ancien = ancien.lower()
    ancien = ancien.translate(str.maketrans(ponctuation))
    ancien = ancien.translate(str.maketrans(accent))
    double_replacer = replacer + replacer
    while double_replacer in ancien:
        ancien = ancien.replace(double_replacer, replacer)
    
    if ancien[0] ==replacer:
        ancien = ancien[1:]
        
    if ancien[-1] == replacer:
        ancien = ancien[:-1]
    
    return ancien


def renameDfCol(df):
    """Description : uniformise le nom des colonnes d'un dataframe en retirant les caractères spéciaux/surabondants
    inputs :
        - df as dataFrame : tableau de données dont les colonnes sont à renommer de manière plus simple
    outputs:
        - dataFrame : tableau de données dont les noms de colonnes ont été modifiés
    """  

    # rename_dict = {ancien:transfoCol(ancien, ponctuation, accent) for ancien in df.columns}
    rename_dict = {ancien:transfoCol(ancien, replacer='_') for ancien in df.columns}
    df_new = df.rename(columns=rename_dict)
    return df_new