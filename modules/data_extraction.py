"""
Data Extraction Module
----------------------
This module retrieves commodity price data from CSV file
based on the commodity selected by the user.
"""

import pandas as pd
import os


def extract_data(commodity):
    """
    Retrieve commodity price data from CSV file.

    Parameters
    ----------
    commodity : str
        Commodity selected by the user.

    Returns
    -------
    pandas.DataFrame
        Raw dataset retrieved from CSV file.
    """

    print("\nReading data from CSV file...")

    # --------------------------------
    # Read CSV File
    # --------------------------------
    csv_path = "reduced_dataset.csv"
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    # Read the entire CSV
    df_all = pd.read_csv(csv_path)
    
    print(f"Total records in CSV: {len(df_all)}")

    # --------------------------------
    # Filter by Commodity
    # --------------------------------
    print(f"Retrieving data for commodity: {commodity}")

    df = df_all[df_all["Commodity"] == commodity][["Arrival_Date", "Modal_Price", "Market"]].copy()

    print(f"Records retrieved: {len(df)}")

    return df