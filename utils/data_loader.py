import pandas as pd

def load_data(uploaded_file):
    """Carga un archivo CSV, Excel o Parquet y devuelve un DataFrame."""
    filename = uploaded_file.name.lower()

    if filename.endswith(".csv"):
        df = pd.read_csv(uploaded_file, encoding='utf-8', low_memory=False)
    elif filename.endswith((".xlsx", ".xls")):
        df = pd.read_excel(uploaded_file)
    elif filename.endswith(".parquet"):
        df = pd.read_parquet(uploaded_file)
    else:
        raise ValueError("Formato de archivo no soportado.")

    return df
