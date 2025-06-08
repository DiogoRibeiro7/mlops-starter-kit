import os
from pathlib import Path
from .config import RAW_DIR, PROCESSED_DIR

def load_raw_data():
    """
    Loads all raw CSV data files from the RAW_DIR directory.

    Returns:
        list: A list containing the data loaded from each CSV file.

    Notes:
        - Assumes RAW_DIR is a predefined directory path.
        - Assumes load_csv is a function that loads a CSV file and returns its contents.
    """
    raw_files = list(Path(RAW_DIR).glob("*.csv"))
    data = [load_csv(file) for file in raw_files]
    return data

def load_csv(path):
    """
    Loads a CSV file into a pandas DataFrame.

    Parameters:
        path (str): The file path to the CSV file.

    Returns:
        pandas.DataFrame: The contents of the CSV file as a DataFrame.
    """
    import pandas as pd
    return pd.read_csv(path)

def save_processed_data(df, filename: str):
    """
    Saves a processed pandas DataFrame to a CSV file in the processed data directory.

    Args:
        df (pandas.DataFrame): The DataFrame to be saved.
        filename (str): The name of the output CSV file.

    Returns:
        pathlib.Path: The path to the saved CSV file.

    Raises:
        OSError: If the directory cannot be created or the file cannot be written.
    """
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    out_path = Path(PROCESSED_DIR) / filename
    df.to_csv(out_path, index=False)
    return out_path

if __name__ == "__main__":
    try:
        # Example script usage
        df_list = load_raw_data()
        # TODO: implement data cleaning and invoke save_processed_data
    except Exception as e:
        print(f"An error occurred: {e}")
    def clean_data(df):
        """
        Placeholder function for data cleaning.

        Args:
            df (pandas.DataFrame): The raw DataFrame to be cleaned.

        Returns:
            pandas.DataFrame: The cleaned DataFrame.
        """
        # Example cleaning step: drop rows with missing values
        return df.dropna()

    # Process and save each DataFrame
    for i, raw_df in enumerate(df_list):
        cleaned_df = clean_data(raw_df)
        save_processed_data(cleaned_df, f"processed_data_{i}.csv")
