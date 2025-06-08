import os
from pathlib import Path
from .config import RAW_DIR, PROCESSED_DIR

def load_raw_data():
    """Load raw data files from RAW_DIR."""
    raw_files = list(Path(RAW_DIR).glob("*.csv"))
    data = [load_csv(file) for file in raw_files]
    return data

def load_csv(path):
    """Utility to load a CSV file into a DataFrame."""
    import pandas as pd
    return pd.read_csv(path)

def save_processed_data(df, filename: str):
    """Save processed DataFrame to PROCESSED_DIR."""
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    out_path = Path(PROCESSED_DIR) / filename
    df.to_csv(out_path, index=False)
    return out_path

if __name__ == "__main__":
    # Example script usage
    df_list = load_raw_data()
    # TODO: implement data cleaning and invoke save_processed_data
