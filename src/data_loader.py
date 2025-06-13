import pandas as pd
import os

def load_data(filepath, delimiter=None):
    """
    Load data from a CSV, TSV, TXT, or Excel file into a pandas DataFrame.
    Allows specifying a delimiter for text files.
    """
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return None
    try:
        ext = os.path.splitext(filepath)[-1].lower()
        if ext in ['.csv']:
            return pd.read_csv(filepath)
        elif ext in ['.tsv']:
            return pd.read_csv(filepath, sep='\t')
        elif ext in ['.xlsx', '.xls']:
            return pd.read_excel(filepath)
        elif ext in ['.txt']:
            # Use provided delimiter or default to '|'
            sep = delimiter if delimiter is not None else '|'
            csv = pd.read_csv(filepath, sep=sep)
            csv.to_csv("../dvc_storage/claims.csv", index=False)
            return csv
        else:
            print(f"Unsupported file extension: {ext}")
            return None
    except Exception as e:
        print(f"Error loading file: {e}")
        return None
