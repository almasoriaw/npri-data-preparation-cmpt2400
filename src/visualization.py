"""
NPRI Data Visualization Module

This module contains functions for visualizing and analyzing
data from the National Pollutant Release Inventory (NPRI).
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Tuple, Dict, Optional, Union


def set_plotting_style():
    """
    Set the default plotting style for consistent visualizations
    """
    sns.set(style="whitegrid")
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 12


def plot_pollutant_trends(df: pd.DataFrame, pollutant_col: str, 
                          year_col: str = 'Reporting_Year', 
                          title: Optional[str] = None) -> plt.Figure:
    """
    Plot trends of a specific pollutant over time
    
    Parameters
    ----------
    df : pd.DataFrame
        NPRI data
    pollutant_col : str
        Column name containing pollutant amounts
    year_col : str, default='Reporting_Year'
        Column name containing reporting years
    title : str, optional
        Plot title
        
    Returns
    -------
    plt.Figure
        The figure containing the plot
    """
    set_plotting_style()
    
    # Group data by year and calculate mean pollutant values
    yearly_data = df.groupby(year_col)[pollutant_col].mean().reset_index()
    
    # Create the plot
    fig, ax = plt.subplots()
    ax.plot(yearly_data[year_col], yearly_data[pollutant_col], 
            marker='o', linestyle='-', linewidth=2)
    
    # Set plot labels and title
    ax.set_xlabel('Year')
    ax.set_ylabel(f'{pollutant_col} (Mean Value)')
    
    if title:
        ax.set_title(title)
    else:
        ax.set_title(f'Trend of {pollutant_col} Over Time')
    
    plt.tight_layout()
    return fig


def plot_provincial_comparison(df: pd.DataFrame, value_col: str, 
                              province_col: str = 'Province',
                              top_n: int = 10,
                              title: Optional[str] = None) -> plt.Figure:
    """
    Create a bar plot comparing provinces by a specific value metric
    
    Parameters
    ----------
    df : pd.DataFrame
        NPRI data
    value_col : str
        Column name containing the values to compare
    province_col : str, default='Province'
        Column name containing province identifiers
    top_n : int, default=10
        Number of top provinces to display
    title : str, optional
        Plot title
        
    Returns
    -------
    plt.Figure
        The figure containing the plot
    """
    set_plotting_style()
    
    # Group data by province and calculate total values
    province_data = df.groupby(province_col)[value_col].sum().sort_values(ascending=False)
    
    # Get top N provinces
    top_provinces = province_data.head(top_n)
    
    # Create the plot
    fig, ax = plt.subplots()
    top_provinces.plot(kind='bar', ax=ax)
    
    # Set plot labels and title
    ax.set_xlabel('Province')
    ax.set_ylabel(f'Total {value_col}')
    
    if title:
        ax.set_title(title)
    else:
        ax.set_title(f'Top {top_n} Provinces by Total {value_col}')
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


def plot_facility_comparisons(df: pd.DataFrame, value_col: str, 
                             facility_col: str = 'Facility_Name',
                             top_n: int = 10,
                             title: Optional[str] = None) -> plt.Figure:
    """
    Create a horizontal bar plot comparing top facilities by a specific value metric
    
    Parameters
    ----------
    df : pd.DataFrame
        NPRI data
    value_col : str
        Column name containing the values to compare
    facility_col : str, default='Facility_Name'
        Column name containing facility identifiers
    top_n : int, default=10
        Number of top facilities to display
    title : str, optional
        Plot title
        
    Returns
    -------
    plt.Figure
        The figure containing the plot
    """
    set_plotting_style()
    
    # Group data by facility and calculate total values
    facility_data = df.groupby(facility_col)[value_col].sum().sort_values(ascending=True)
    
    # Get top N facilities
    top_facilities = facility_data.tail(top_n)
    
    # Create the plot
    fig, ax = plt.subplots()
    top_facilities.plot(kind='barh', ax=ax)
    
    # Set plot labels and title
    ax.set_ylabel('Facility')
    ax.set_xlabel(f'Total {value_col}')
    
    if title:
        ax.set_title(title)
    else:
        ax.set_title(f'Top {top_n} Facilities by Total {value_col}')
    
    plt.tight_layout()
    return fig


def plot_pollutant_distribution(df: pd.DataFrame, pollutant_col: str,
                               log_scale: bool = False,
                               title: Optional[str] = None) -> plt.Figure:
    """
    Create a histogram showing the distribution of a pollutant
    
    Parameters
    ----------
    df : pd.DataFrame
        NPRI data
    pollutant_col : str
        Column name containing pollutant amounts
    log_scale : bool, default=False
        Whether to use a logarithmic scale for the x-axis
    title : str, optional
        Plot title
        
    Returns
    -------
    plt.Figure
        The figure containing the plot
    """
    set_plotting_style()
    
    # Create the plot
    fig, ax = plt.subplots()
    
    # Remove zero or negative values if using log scale
    plot_data = df[pollutant_col]
    if log_scale:
        plot_data = plot_data[plot_data > 0]
    
    # Create histogram
    sns.histplot(plot_data, kde=True, ax=ax)
    
    # Set logarithmic scale if requested
    if log_scale:
        ax.set_xscale('log')
    
    # Set plot labels and title
    ax.set_xlabel(pollutant_col)
    ax.set_ylabel('Frequency')
    
    if title:
        ax.set_title(title)
    else:
        ax.set_title(f'Distribution of {pollutant_col}')
    
    plt.tight_layout()
    return fig
