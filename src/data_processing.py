"""
NPRI Data Processing Module

This module contains functions for loading, cleaning, and preprocessing
data from the National Pollutant Release Inventory (NPRI).
"""

import pandas as pd
import numpy as np
import os
from typing import Tuple, List, Dict, Optional, Union


def load_npri_data(file_path: str) -> pd.DataFrame:
    """
    Load NPRI data from various file formats (CSV, Excel)
    
    Parameters
    ----------
    file_path : str
        Path to the NPRI data file
        
    Returns
    -------
    pd.DataFrame
        Loaded NPRI data
    """
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.csv':
        df = pd.read_csv(file_path, low_memory=False)
    elif file_extension in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")
    
    print(f"Loaded data with {df.shape[0]} rows and {df.shape[1]} columns")
    return df


def clean_npri_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean NPRI data by handling missing values, standardizing column names,
    and filtering invalid entries
    
    Parameters
    ----------
    df : pd.DataFrame
        Raw NPRI data
        
    Returns
    -------
    pd.DataFrame
        Cleaned NPRI data
    """
    # Make a copy to avoid modifying the original dataframe
    df_clean = df.copy()
    
    # Standardize column names
    df_clean.columns = [col.strip().replace(' ', '_') for col in df_clean.columns]
    
    # Convert reporting year to numeric if it exists
    if 'Reporting_Year' in df_clean.columns:
        df_clean['Reporting_Year'] = pd.to_numeric(df_clean['Reporting_Year'], errors='coerce')
    
    # Remove rows with all NaN values
    df_clean = df_clean.dropna(how='all')
    
    # Reset index
    df_clean = df_clean.reset_index(drop=True)
    
    return df_clean


def filter_by_year(df: pd.DataFrame, year: int) -> pd.DataFrame:
    """
    Filter NPRI data for a specific reporting year
    
    Parameters
    ----------
    df : pd.DataFrame
        NPRI data
    year : int
        Reporting year to filter for
        
    Returns
    -------
    pd.DataFrame
        Filtered NPRI data for the specified year
    """
    if 'Reporting_Year' not in df.columns:
        raise ValueError("DataFrame does not contain 'Reporting_Year' column")
    
    return df[df['Reporting_Year'] == year].reset_index(drop=True)


def filter_by_province(df: pd.DataFrame, province: str) -> pd.DataFrame:
    """
    Filter NPRI data for a specific province
    
    Parameters
    ----------
    df : pd.DataFrame
        NPRI data
    province : str
        Province code to filter for (e.g., 'ON', 'AB')
        
    Returns
    -------
    pd.DataFrame
        Filtered NPRI data for the specified province
    """
    if 'Province' not in df.columns:
        raise ValueError("DataFrame does not contain 'Province' column")
    
    return df[df['Province'] == province].reset_index(drop=True)


def prepare_data_for_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare the NPRI data for analysis by:
    - Converting columns to appropriate data types
    - Adding derived columns
    - Handling outliers
    
    Parameters
    ----------
    df : pd.DataFrame
        Cleaned NPRI data
        
    Returns
    -------
    pd.DataFrame
        NPRI data prepared for analysis
    """
    df_prep = df.copy()
    
    # Numeric columns to convert
    numeric_cols = ['Reporting_Year', 'NPRI_ID']
    
    # Convert numeric columns
    for col in numeric_cols:
        if col in df_prep.columns:
            df_prep[col] = pd.to_numeric(df_prep[col], errors='coerce')
    
    # Add current year for age calculation
    if 'Reporting_Year' in df_prep.columns:
        current_year = pd.Timestamp.now().year
        df_prep['Years_Since_Report'] = current_year - df_prep['Reporting_Year']
    
    return df_prep
