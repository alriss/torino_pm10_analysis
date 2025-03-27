import statsmodels.api as sm
import numpy as np

from utils import pretty_pvalue
from visualization import plot_correlation
from statsmodels.tsa.stattools import grangercausalitytests
from scipy.stats import spearmanr
from scipy.signal import correlate


def granger_test(df, v_maxlag):
    """Test di causalità di Granger."""
    print(f"\nGranger Causality Test: {df.columns[0]} vs {df.columns[1]}")
    result = grangercausalitytests(df, maxlag=v_maxlag)
    return result

def regression_analysis(df):
    """Regressione multipla tra PM10, pioggia e temperatura."""
    X = df.iloc[:,1:]
    X = sm.add_constant(X)
    y = df.iloc[:,0]
    model = sm.OLS(y, X).fit()
    print(model.summary())

def correlation_tests(df):
    """Calcola la correlazione di Spearman e Kendall."""
    print(f"\nCorrelazione {df.columns[0]} vs {df.columns[1]}")
    rho, pval = spearmanr(df.iloc[:, 0], df.iloc[:, 1])
    print(f"Spearman rho: {rho:.3f}, p-value: {pretty_pvalue(pval)}")

def cross_correlation(df,max_lag):
    print('\n\nCross-correlation function')
    pm10_series = df.iloc[:,0] - np.mean(df.iloc[:,0])
    rain_series = df.iloc[:,1] - np.mean(df.iloc[:,1])

    ccf = correlate(pm10_series, rain_series, mode='full')
    ccf = ccf / (np.std(pm10_series) * np.std(rain_series) * len(pm10_series))
    lags = np.arange(-len(pm10_series) + 1, len(pm10_series))

    min_lag = 0
     

    lag_mask = (lags >= min_lag) & (lags <= max_lag)

    lags = lags[lag_mask]
    ccf = ccf[lag_mask]

    rho, pval = spearmanr(df.iloc[:, 0], df.iloc[:, 1])
    result = grangercausalitytests(df, max_lag, verbose=False)

    tests = ['ssr_ftest', 'ssr_chi2test', 'lrtest', 'params_ftest']
    pvals = [pretty_pvalue(pval)] + [pretty_pvalue(max([val[0][tests[0]][1],val[0][tests[1]][1],val[0][tests[2]][1],val[0][tests[3]][1]])) for val in result.values()]

    plot_correlation(df,lags,ccf, pvals)

    