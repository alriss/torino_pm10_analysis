from utils import load_pm10_data,load_beta_pm10_data, load_prec_data, load_temp_data
from visualization import plot_pm10, plotmissingval
from statistical_tests import correlation_tests, regression_analysis, cross_correlation
import pandas as pd
import numpy as np
import sys

temp_thr = 6 # Temperatura di soglia

path_pm10 = '../data/Torino_Lingotto_PM10_2024.csv'
path_prec = '../data/Torino_Vallere_precipitazioni_2024.csv'
path_temp = '../data/Torino_Vallere_temperature_2024.csv'

df_pm10   = load_pm10_data(path_pm10)
df_piogge = load_prec_data(path_prec)
df_temp   = load_temp_data(path_temp, temp_thr)

plot_pm10(df_pm10, df_piogge, df_temp, temp_thr)

df_corr = pd.concat([df_pm10['Valore'], df_piogge['Pioggia'], df_temp['Minima sotto soglia']], axis=1)
df_corr.columns = ['PM10', 'Pioggia', 'Temperatura']
df_corr.index = df_pm10['Data rilevamento']

# Visualizzazione dei valori nulli

plotmissingval(df_corr)

# I valori nulli vengono rimpiazzati con i pm10 beta (misure meno accurate)

beta_pm10 = load_beta_pm10_data(path_pm10)
beta_pm10 = beta_pm10.set_index(df_corr.index)  # Allinea gli indici
df_corr.loc[~np.isfinite(df_corr['PM10']), 'PM10'] = beta_pm10.loc[~np.isfinite(df_corr['PM10']), 'Valore']

plotmissingval(df_corr)

beta_pm10 = beta_pm10.set_index(df_pm10.index)  # Allinea gli indici
null_vals = ~np.isfinite(df_pm10['Valore'])
df_pm10[null_vals] = beta_pm10[null_vals]

plot_pm10(df_pm10, df_piogge, df_temp, temp_thr, beta=True, null_vals = null_vals)

old_stdout = sys.stdout
log_file = open("../output.log","w")

sys.stdout = log_file

# Test di Spearman
# Correlazioni non lineari

mask = np.isfinite(df_corr['PM10']) # Rimozione dei valori nulli (non influenza la correlazione non lineare)

correlation_tests(df_corr[mask][['PM10', 'Pioggia']])
correlation_tests(df_corr[mask][['PM10', 'Temperatura']])

# Analisi di causalità di Granger
# Prevedibilità dei livelli di PM10 in base a fattori esterni

# Imputazione dei valori nulli: interpolazione lineare e backfilling (necessario per la regressione lineare)
df_corr['PM10'] = df_corr['PM10'].interpolate(method='linear').ffill().bfill()

# Regressione multivariata
# Impatto combinato di più fattori sul PM10

regression_analysis(df_corr[mask])

# Cross-correlation function (CCF): per analizzare il ritardo temporale tra eventi esterni e variazioni di PM10.
cross_correlation(df_corr[['PM10', 'Pioggia']], 40)
cross_correlation(df_corr[['PM10', 'Temperatura']], 20)

sys.stdout = old_stdout
log_file.close()