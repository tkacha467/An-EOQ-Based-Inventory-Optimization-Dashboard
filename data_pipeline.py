"""
Data Pipeline Module for Smart Inventory Advisor.

Handles data cleaning, validation, field mapping, and transformation from
the raw Kaggle High-Dimensional Supply Chain Inventory Dataset to the standard EOQ model input.
"""

import pandas as pd
import numpy as np
import os
import eoq_model

RAW_DATA_PATH = "data/raw_supply_chain_dataset.csv"
PROCESSED_DATA_PATH = "data/inventory_data.csv"
DEFAULT_HOLDING_RATE = 0.20  # 20% annual inventory carrying cost rate (i) on unit manufacturing cost (C)


def process_raw_dataset(raw_df: pd.DataFrame, holding_rate: float = DEFAULT_HOLDING_RATE) -> pd.DataFrame:
    """
    Cleans raw supply chain dataset and maps fields to EOQ model inputs:
      - Product <- SKU
      - Annual_Demand <- Number of products sold
      - Ordering_Cost <- Shipping costs
      - Holding_Cost <- DERIVED: Manufacturing costs * holding_rate (H = i * C)
      - Lead_Time_Days <- Lead times
    """
    if raw_df is None or raw_df.empty:
        raise ValueError("Input dataset is empty.")

    # Drop exact duplicate rows if any
    df = raw_df.drop_duplicates().copy()

    # Check if df is already in EOQ format
    eoq_cols = ['Product', 'Annual_Demand', 'Ordering_Cost', 'Holding_Cost', 'Lead_Time_Days']
    if all(col in df.columns for col in eoq_cols):
        eoq_model.validate_input_dataframe(df[eoq_cols])
        return df[eoq_cols].copy()

    # Required Kaggle fields
    kaggle_cols = ['SKU', 'Number of products sold', 'Shipping costs', 'Manufacturing costs', 'Lead times']
    missing = [col for col in kaggle_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Dataset is missing required Kaggle fields: {', '.join(missing)}")

    # Clean numeric fields
    for col in ['Number of products sold', 'Shipping costs', 'Manufacturing costs', 'Lead times']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Remove rows with NaN or non-positive values in required fields
    df = df.dropna(subset=kaggle_cols)
    df = df[
        (df['Number of products sold'] > 0) &
        (df['Shipping costs'] > 0) &
        (df['Manufacturing costs'] > 0) &
        (df['Lead times'] > 0)
    ]

    if df.empty:
        raise ValueError("No valid records remain after cleaning and zero/negative value filtering.")

    # Construct EOQ dataframe
    eoq_df = pd.DataFrame()
    
    # If 'Product type' exists, append it for clear identification
    if 'Product type' in df.columns:
        eoq_df['Product'] = df['SKU'].astype(str) + " (" + df['Product type'].astype(str).str.title() + ")"
    else:
        eoq_df['Product'] = df['SKU'].astype(str)

    eoq_df['Annual_Demand'] = df['Number of products sold'].astype(float)
    eoq_df['Ordering_Cost'] = df['Shipping costs'].astype(float)
    eoq_df['Holding_Cost'] = (df['Manufacturing costs'] * holding_rate).astype(float)
    eoq_df['Lead_Time_Days'] = df['Lead times'].astype(float)

    # Validate resulting dataframe
    eoq_model.validate_input_dataframe(eoq_df)

    return eoq_df


def load_and_prepare_data(holding_rate: float = DEFAULT_HOLDING_RATE) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Loads raw Kaggle dataset, runs the data pipeline, and returns (raw_df, eoq_input_df).
    """
    if not os.path.exists(RAW_DATA_PATH):
        import data_generator
        data_generator.generate_or_load_raw_kaggle_dataset(RAW_DATA_PATH)

    raw_df = pd.read_csv(RAW_DATA_PATH)
    eoq_df = process_raw_dataset(raw_df, holding_rate=holding_rate)
    
    # Save processed dataframe for caching/default use
    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
    eoq_df.to_csv(PROCESSED_DATA_PATH, index=False)
    
    return raw_df, eoq_df


if __name__ == '__main__':
    raw_df, eoq_df = load_and_prepare_data()
    print(f"Data pipeline executed successfully!")
    print(f"Raw rows: {len(raw_df)}, Processed SKUs: {len(eoq_df)}")
    print(eoq_df.head(5).to_string(index=False))
