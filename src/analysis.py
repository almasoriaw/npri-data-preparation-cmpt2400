"""
NPRI Data Analysis Module

This module contains functions for statistical analysis and insights
generation from the National Pollutant Release Inventory (NPRI) data.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional, Union
from scipy import stats


def summarize_pollutants(df: pd.DataFrame, pollutant_col: str, 
                        groupby_col: Optional[str] = None) -> pd.DataFrame:
    """
    Generate summary statistics for pollutants
    
    Parameters
    ----------
    df : pd.DataFrame
        NPRI data
    pollutant_col : str
        Column name containing pollutant amounts
    groupby_col : str, optional
        Column to group by (e.g., 'Province', 'NAICS')
        
    Returns
    -------
    pd.DataFrame
        Summary statistics for the pollutant
    """
    if groupby_col:
        summary = df.groupby(groupby_col)[pollutant_col].agg([
            'count', 'mean', 'std', 'min', 
            lambda x: x.quantile(0.25),
            'median',
            lambda x: x.quantile(0.75),
            'max'
        ])
        
        # Rename columns
        summary.columns = ['Count', 'Mean', 'Std', 'Min', 'Q1', 'Median', 'Q3', 'Max']
        
    else:
        summary = pd.DataFrame({
            'Count': df[pollutant_col].count(),
            'Mean': df[pollutant_col].mean(),
            'Std': df[pollutant_col].std(),
            'Min': df[pollutant_col].min(),
            'Q1': df[pollutant_col].quantile(0.25),
            'Median': df[pollutant_col].median(),
            'Q3': df[pollutant_col].quantile(0.75),
            'Max': df[pollutant_col].max()
        }, index=[pollutant_col])
    
    return summary


def identify_outliers(df: pd.DataFrame, column: str, 
                     method: str = 'iqr', threshold: float = 1.5) -> pd.DataFrame:
    """
    Identify outliers in a specific column using IQR or Z-score method
    
    Parameters
    ----------
    df : pd.DataFrame
        NPRI data
    column : str
        Column to check for outliers
    method : str, default='iqr'
        Method to use for outlier detection ('iqr' or 'zscore')
    threshold : float, default=1.5
        Threshold for outlier detection (1.5 for IQR, 3.0 for Z-score recommended)
        
    Returns
    -------
    pd.DataFrame
        DataFrame with outliers
    """
    if method.lower() == 'iqr':
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
        
    elif method.lower() == 'zscore':
        z_scores = np.abs(stats.zscore(df[column].dropna()))
        outliers_idx = np.where(z_scores > threshold)[0]
        outliers = df.iloc[outliers_idx]
        
    else:
        raise ValueError("Method must be 'iqr' or 'zscore'")
    
    return outliers


def trend_analysis(df: pd.DataFrame, value_col: str, 
                  year_col: str = 'Reporting_Year', 
                  groupby_col: Optional[str] = None) -> pd.DataFrame:
    """
    Analyze trends over time for a specific value, optionally grouped by a category
    
    Parameters
    ----------
    df : pd.DataFrame
        NPRI data
    value_col : str
        Column name containing the values to analyze
    year_col : str, default='Reporting_Year'
        Column containing year information
    groupby_col : str, optional
        Column to group by for separate trend analysis
        
    Returns
    -------
    pd.DataFrame
        Trend analysis results with year-over-year changes
    """
    # Ensure year column is sorted
    df = df.sort_values(by=year_col)
    
    if groupby_col:
        # Group by year and the specified column
        grouped = df.groupby([year_col, groupby_col])[value_col].mean().reset_index()
        
        # Calculate year-over-year change for each group
        trend_df = pd.DataFrame()
        
        for group in grouped[groupby_col].unique():
            group_data = grouped[grouped[groupby_col] == group].copy()
            
            # Calculate absolute change
            group_data['Absolute_Change'] = group_data[value_col].diff()
            
            # Calculate percentage change
            group_data['Percent_Change'] = group_data[value_col].pct_change() * 100
            
            trend_df = pd.concat([trend_df, group_data])
            
    else:
        # Group by year only
        grouped = df.groupby(year_col)[value_col].mean().reset_index()
        
        # Calculate year-over-year changes
        trend_df = grouped.copy()
        trend_df['Absolute_Change'] = trend_df[value_col].diff()
        trend_df['Percent_Change'] = trend_df[value_col].pct_change() * 100
    
    return trend_df


def compare_categories(df: pd.DataFrame, value_col: str, 
                      category_col: str, 
                      year_col: Optional[str] = 'Reporting_Year', 
                      year_filter: Optional[int] = None) -> pd.DataFrame:
    """
    Compare different categories (e.g., provinces, industries) based on a value metric
    
    Parameters
    ----------
    df : pd.DataFrame
        NPRI data
    value_col : str
        Column name containing the values to compare
    category_col : str
        Column containing categories to compare
    year_col : str, optional, default='Reporting_Year'
        Column containing year information
    year_filter : int, optional
        Specific year to filter data for
        
    Returns
    -------
    pd.DataFrame
        Comparison results for different categories
    """
    # Filter for specific year if provided
    if year_filter and year_col in df.columns:
        df_filtered = df[df[year_col] == year_filter]
    else:
        df_filtered = df.copy()
    
    # Group by category and calculate statistics
    category_stats = df_filtered.groupby(category_col)[value_col].agg([
        'count', 'sum', 'mean', 'median', 'std'
    ]).reset_index()
    
    # Sort by sum in descending order
    category_stats = category_stats.sort_values(by='sum', ascending=False)
    
    # Calculate percentage of total
    total_sum = category_stats['sum'].sum()
    category_stats['percent_of_total'] = (category_stats['sum'] / total_sum) * 100
    
    # Add cumulative percentage
    category_stats['cumulative_percent'] = category_stats['percent_of_total'].cumsum()
    
    return category_stats
