# NPRI Data Preparation and Analysis

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Data Source](https://img.shields.io/badge/data%20source-NPRI-orange)

## 📋 Project Overview

This project focuses on the preparation, cleaning, and analysis of Canada's National Pollutant Release Inventory (NPRI) data. The NPRI is Canada's public inventory of pollutant releases, disposals, and transfers for recycling, providing valuable information about pollution across the country.

## 🔍 Key Features

- **Comprehensive Data Processing Pipeline**: Tools for loading, cleaning, and preprocessing NPRI data
- **Statistical Analysis**: Functions for trend analysis, outlier detection, and comparative statistics
- **Visualization Suite**: Various plotting functions for analyzing pollutant trends, provincial comparisons, and facility rankings
- **Modular Architecture**: Well-organized codebase with separate modules for data processing, analysis, and visualization

## 🔧 Technologies & Libraries

This project leverages the following Python libraries:

- **pandas & numpy**: Core data manipulation and numerical processing
- **matplotlib & seaborn**: Data visualization and statistical graphics
- **scipy & statsmodels**: Statistical analysis and hypothesis testing
- **geopandas**: Geographic data processing for spatial analysis
- **plotly**: Interactive visualizations (when needed)
- **scikit-learn**: For any machine learning implementations
- **jupyter**: Interactive development and documentation

## 🗂️ Project Structure

```
npri-data-preparation-cmpt2400/
├── data/
│   ├── raw/           # Original unmodified NPRI datasets
│   ├── interim/       # Intermediate data that has been transformed
│   └── processed/     # Final, canonical data sets for analysis
│
├── docs/              # Documentation files
│
├── notebooks/         # Jupyter notebooks for exploration and analysis
│   ├── 01_NPRI_Dataset_Cleaning_EDA.ipynb
│   ├── 02_Transition_Analysis.ipynb
│   └── 03_Final_Analysis.ipynb
│
├── src/               # Source code for use in this project
│   ├── __init__.py
│   ├── data_processing.py  # Functions for data loading and preprocessing
│   ├── analysis.py         # Statistical analysis functions
│   └── visualization.py    # Data visualization functions
│
├── models/            # Trained models or analysis results
│
├── .gitignore         # Files to ignore in version control
├── LICENSE            # Project license
├── README.md          # The top-level README
└── requirements.txt   # Dependencies
```

## 📊 Data Sources

The project uses data from Canada's National Pollutant Release Inventory (NPRI), which includes:

- Pollutant release information from 1993 to present
- Facility and company information
- Geographical data on pollution sources
- Industry classification (NAICS) data

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/almasoriaw/npri-data-preparation-cmpt2400.git
   cd npri-data-preparation-cmpt2400
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Data Acquisition

The NPRI datasets are available through the Government of Canada's Open Data Portal. Due to their large size, they are not included in this repository but can be downloaded using the following steps:

1. Visit the [NPRI Open Data Portal](https://open.canada.ca/data/en/dataset/40e01423-7728-429c-ac9d-2954385ccdfb)
2. Download the desired datasets
3. Place the raw data files in the `data/raw/` directory

## 📈 Usage Examples

### Loading and Processing Data

```python
from src.data_processing import load_npri_data, clean_npri_data

# Load raw NPRI data
raw_data = load_npri_data('data/raw/NPRI_Releases_1993-present.csv')

# Clean the data
cleaned_data = clean_npri_data(raw_data)

# Filter for a specific year
data_2020 = filter_by_year(cleaned_data, 2020)
```

### Analyzing Pollutant Trends

```python
from src.analysis import trend_analysis, compare_categories

# Analyze trends of a specific pollutant over time
co2_trends = trend_analysis(cleaned_data, 'CO2_Emissions', groupby_col='Province')

# Compare provinces by total emissions
province_comparison = compare_categories(cleaned_data, 'Total_Emissions', 'Province')
```

### Creating Visualizations

```python
from src.visualization import plot_pollutant_trends, plot_provincial_comparison

# Plot trends of CO2 emissions over time
fig = plot_pollutant_trends(cleaned_data, 'CO2_Emissions', 
                          title='CO2 Emission Trends (1993-2022)')

# Compare top provinces by total emissions
fig = plot_provincial_comparison(cleaned_data, 'Total_Emissions')
```

## 📚 Documentation

For more detailed documentation:

- See the `docs/` directory for additional documentation
- Check the Jupyter notebooks in `notebooks/` for exploratory analyses and examples
- Review the docstrings in each module for function-specific documentation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- The [National Pollutant Release Inventory](https://www.canada.ca/en/environment-climate-change/services/national-pollutant-release-inventory.html) for providing open access to pollution data
- The Canadian government's open data initiative for making environmental data accessible
