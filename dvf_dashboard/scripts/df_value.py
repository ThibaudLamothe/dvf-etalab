import pickle
import pandas as pd
from scripts import dvf_functions

print('*'*50, ' Loading Start ', '*'*50,)
#df_dvf = pd.read_csv('/Users/thibaudlamothe/OneDrive - Capgemini/Documents/Data/DVF/data_per_dept/processed_2018/dept_35.csv')
#df_immo = pickle.load(open('C:/Users/Thibaud Lamothe/Documents/Python/10_lbc_scrap/02_analysis/df.p', 'rb'))
#df_new = pickle.load(open('C:/Users/Thibaud Lamothe/Documents/Python/10_lbc_scrap/02_analysis/df_new.p', 'rb'))
#df_old = pickle.load(open('C:/Users/Thibaud Lamothe/Documents/Python/10_lbc_scrap/02_analysis/df_old.p', 'rb'))

rep = dvf_functions.preparingData(pick=True)
print('*'*50, ' Loading Finished ' ,'*'*50,)



