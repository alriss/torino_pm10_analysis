from utils import load_pm10_data, load_prec_data, load_temp_data
from visualization import plot_pm10
from statistical_tests import granger_test, correlation_tests, regression_analysis, cross_correlation
import pandas as pd
import numpy as np

temp_thr = 6 # Temperatura di soglia

df_pm10   = load_pm10_data('../data/Torino_Lingotto_PM10_2024.csv')
df_piogge = load_prec_data('../data/Torino_Vallere_precipitazioni_2024.csv')
df_temp   = load_temp_data('../data/Torino_Vallere_temperature_2024.csv', temp_thr)

plot_pm10(df_pm10, df_piogge, df_temp, temp_thr)

df_corr = pd.concat([df_pm10['Valore'], df_piogge['Pioggia'], df_temp['Minima sotto soglia']], axis=1)
df_corr.columns = ['PM10', 'Pioggia', 'Temperatura']

# Test di Spearman
# Correlazioni non lineari

mask = np.isfinite(df_corr['PM10']) # Rimozione dei valori nulli (non influenza la correlazione)

correlation_tests(df_corr[mask][['PM10', 'Pioggia']])
correlation_tests(df_corr[mask][['PM10', 'Temperatura']])

# Analisi di causalità di Granger
# Prevedibilità dei livelli di PM10 in base a fattori esterni

# Imputazione dei valori nulli: interpolazione lineare e backfilling (necessario per il test di Granger)
df_corr['PM10'] = df_corr['PM10'].interpolate(method='linear').ffill().bfill()
df_corr['Pioggia'] = df_corr['Pioggia'].interpolate(method='linear').ffill().bfill()
df_corr['Temperatura'] = df_corr['Temperatura'].interpolate(method='linear').ffill().bfill()

granger_test(df_corr[['PM10', 'Pioggia']], v_maxlag=3)
granger_test(df_corr[['PM10', 'Temperatura']], v_maxlag=3)

# Regressione multivariata
# Impatto combinato di più fattori sul PM10

regression_analysis(df_corr[mask])

# Cross-correlation function (CCF): per analizzare il ritardo temporale tra eventi esterni e variazioni di PM10.
cross_correlation(df_corr[['PM10', 'Pioggia']], 40)
cross_correlation(df_corr[['PM10', 'Temperatura']], 20)
