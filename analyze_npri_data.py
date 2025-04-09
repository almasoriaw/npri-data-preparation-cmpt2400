"""
NPRI Data Analysis Script

This script demonstrates how to use the NPRI data preparation modules
to load, process, analyze, and visualize NPRI data.

Usage:
    python analyze_npri_data.py --data_path=data/raw/NPRI_Releases_1993-present.csv --year=2020

"""

import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
import sys

# Add the project directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import project modules
from src.data_processing import load_npri_data, clean_npri_data, filter_by_year, filter_by_province
from src.analysis import summarize_pollutants, trend_analysis, compare_categories
from src.visualization import plot_pollutant_trends, plot_provincial_comparison, plot_facility_comparisons


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Analyze NPRI data')
    parser.add_argument('--data_path', type=str, required=True,
                        help='Path to the NPRI data file')
    parser.add_argument('--year', type=int, 
                        help='Specific year to analyze')
    parser.add_argument('--province', type=str,
                        help='Province code to filter (e.g., ON, AB)')
    parser.add_argument('--pollutant_col', type=str, default='Total_Release',
                        help='Column name for pollutant values')
    parser.add_argument('--output_dir', type=str, default='output',
                        help='Directory to save output files')
    return parser.parse_args()


def main():
    """Main function to run the analysis."""
    # Parse arguments
    args = parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    print(f"Loading data from {args.data_path}...")
    
    try:
        # Load and clean data
        raw_data = load_npri_data(args.data_path)
        print(f"Loaded {raw_data.shape[0]} records with {raw_data.shape[1]} columns")
        
        cleaned_data = clean_npri_data(raw_data)
        print(f"Cleaned data has {cleaned_data.shape[0]} valid records")
        
        # Filter data if year or province is specified
        if args.year:
            print(f"Filtering data for year {args.year}")
            filtered_data = filter_by_year(cleaned_data, args.year)
        elif args.province:
            print(f"Filtering data for province {args.province}")
            filtered_data = filter_by_province(cleaned_data, args.province)
        else:
            filtered_data = cleaned_data.copy()
            
        print(f"Working with {filtered_data.shape[0]} records after filtering")
        
        # Summary statistics
        print("\nGenerating summary statistics...")
        summary = summarize_pollutants(filtered_data, args.pollutant_col)
        summary_path = os.path.join(args.output_dir, 'pollutant_summary.csv')
        summary.to_csv(summary_path)
        print(f"Summary statistics saved to {summary_path}")
        
        # Trend analysis if we have multiple years
        if 'Reporting_Year' in filtered_data.columns and len(filtered_data['Reporting_Year'].unique()) > 1:
            print("\nPerforming trend analysis...")
            trends = trend_analysis(filtered_data, args.pollutant_col)
            trends_path = os.path.join(args.output_dir, 'pollutant_trends.csv')
            trends.to_csv(trends_path)
            print(f"Trend analysis saved to {trends_path}")
            
            # Plot trends
            print("Creating trend visualization...")
            fig = plot_pollutant_trends(filtered_data, args.pollutant_col)
            fig_path = os.path.join(args.output_dir, 'pollutant_trend.png')
            fig.savefig(fig_path)
            print(f"Trend visualization saved to {fig_path}")
        
        # Provincial comparison if province column exists
        if 'Province' in filtered_data.columns:
            print("\nComparing provinces...")
            province_stats = compare_categories(filtered_data, args.pollutant_col, 'Province')
            province_path = os.path.join(args.output_dir, 'province_comparison.csv')
            province_stats.to_csv(province_path)
            print(f"Provincial comparison saved to {province_path}")
            
            # Plot provincial comparison
            print("Creating provincial comparison visualization...")
            fig = plot_provincial_comparison(filtered_data, args.pollutant_col)
            fig_path = os.path.join(args.output_dir, 'province_comparison.png')
            fig.savefig(fig_path)
            print(f"Provincial comparison visualization saved to {fig_path}")
        
        # Facility comparison
        if 'Facility_Name' in filtered_data.columns:
            print("\nComparing top facilities...")
            fig = plot_facility_comparisons(filtered_data, args.pollutant_col)
            fig_path = os.path.join(args.output_dir, 'facility_comparison.png')
            fig.savefig(fig_path)
            print(f"Facility comparison visualization saved to {fig_path}")
        
        print("\nAnalysis completed successfully!")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
