import pandas as pd

def load_pm10_data(filepath):
    """Carica il file CSV contenente i dati PM10."""
    df = pd.read_csv(filepath, index_col=False, delimiter=";")
    df["Data rilevamento"] = pd.to_datetime(df["Data rilevamento"], format="%d/%m/%Y")
    df = df[df["Id Parametro"] == "PM10_GBV"]
    return df[df["Id Parametro"] == "PM10_GBV"]

def load_prec_data(filepath):
    """Carica il file CSV con i dati delle precipitazioni."""
    df = pd.read_csv(filepath, index_col=False, delimiter=",")
    df["DATA"] = pd.to_datetime(df["DATA"], format="%Y-%m-%d")
    df = pd.concat([df[["DATA", "Precipitazione (mm)"]],pd.Series([1 if float(i) > 0 else 0 for i in df["Precipitazione (mm)"]])], axis=1)
    df.columns = ["DATA", "Precipitazione (mm)", "Pioggia"]
    return df

def load_temp_data(filepath, temp_thr=6):
    """Carica il file CSV con i dati delle temperature minime."""
    df = pd.read_csv(filepath, index_col=False, delimiter=",")
    df["DATA"] = pd.to_datetime(df["DATA"], format="%Y-%m-%d")
    df = pd.concat([df[["DATA", "Temperatura minima"]],pd.Series([1 if float(i) < temp_thr else 0 for i in df["Temperatura minima"]])], axis=1)
    df.columns = ["DATA", "Temperatura minima", "Minima sotto soglia"]
    return df

def pretty_pvalue(pvalue):
    if pvalue < 0.0001:
        return "****"
    elif pvalue < 0.001:
        return "***"
    elif pvalue < 0.01:
        return "**"
    elif pvalue < 0.05:
        return "*"
    else:
        return ""  # Not significant
    