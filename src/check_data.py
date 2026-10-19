
import pandas as pd
from pathlib import Path

file_path = Path("data/raw/Online Retail.xlsx")

print("Loading retail dataset...")
df = pd.read_excel(file_path)

print("\n========== DATASET OVERVIEW ==========")
print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])

print("\n========== COLUMN DATA TYPES ==========")
print(df.dtypes)

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

print("\n========== DUPLICATE ROWS ==========")
print("Duplicate rows:", df.duplicated().sum())

print("\n========== TRANSACTION DETAILS ==========")
print("Unique invoices:", df["InvoiceNo"].nunique())
print("Unique products:", df["StockCode"].nunique())
print("Unique customers:", df["CustomerID"].nunique())
print("Unique countries:", df["Country"].nunique())

print("\n========== QUANTITY AND PRICE ==========")
print(df[["Quantity", "UnitPrice"]].describe())

print("\n========== CANCELLED INVOICES ==========")
cancelled = df["InvoiceNo"].astype(str).str.startswith("C")
print("Rows with cancelled invoice IDs:", cancelled.sum())

print("\nData-quality inspection completed!")
