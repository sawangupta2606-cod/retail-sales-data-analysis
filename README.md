# Retail Sales Data Analysis Using Python

An end-to-end data analytics project that analyzes retail transactions to identify sales trends, top-performing products, customer purchasing patterns, and country-wise revenue.

## Project Overview

This project uses Python to clean, process, analyze, and visualize retail sales data. It includes an interactive Streamlit dashboard to explore business performance and generate useful insights from transaction data.

## Technologies Used

- **Python** — Core programming
- **Pandas & NumPy** — Data cleaning and analysis
- **Matplotlib & Seaborn** — Data visualization
- **Streamlit** — Interactive dashboard
- **Excel / CSV** — Data storage and processed reports

## Key Features

- Data quality checks and duplicate removal
- Handling missing values and identifying cancelled orders and returns
- Monthly sales trend analysis
- Top-performing product analysis
- Country-wise revenue comparison
- Customer analysis and repeat-purchase insights
- Interactive dashboard with filters and key performance indicators

## Key Findings

- **Total sales revenue:** £10.64 million
- **Valid invoices analyzed:** 20,726
- **Customers analyzed:** 4,339
- **Repeat-customer rate:** 65.57%
- **Highest-revenue month:** November 2011

*Note: Revenue is calculated from eligible positive-quantity sales transactions. Returns and cancelled invoices are excluded.*

## Project Structure

```text
retail-sales-data-analysis/
├── dashboard/
│   └── app.py
├── data/
│   ├── raw/
│   └── processed/
├── outputs/
│   ├── figures/
│   └── reports/
├── src/
│   ├── check_data.py
│   ├── clean_data.py
│   ├── sales_analysis.py
│   ├── product_country_analysis.py
│   ├── customer_analysis.py
│   ├── visualize_customers.py
│   └── visualize_performance.py
├── requirements.txt
├── README.md
└── .gitignore
```

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/sawangupta2606-cod/retail-sales-data-analysis.git
cd retail-sales-data-analysis
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the dataset

Download the **Online Retail** dataset from the UCI Machine Learning Repository and place `Online Retail.xlsx` inside `data/raw/`.

Dataset source: https://archive.ics.uci.edu/dataset/352/online+retail

### 5. Clean and analyze the data

```bash
python src/clean_data.py
python src/sales_analysis.py
python src/product_country_analysis.py
python src/customer_analysis.py
```

### 6. Launch the dashboard

```bash
python -m streamlit run dashboard/app.py
```

## Project Goal

The goal of this project is to demonstrate practical data analytics skills, including data cleaning, exploratory data analysis, business insight generation, visualization, and interactive dashboard development.

## Author

Sawan Gupta

GitHub: https://github.com/sawangupta2606-cod