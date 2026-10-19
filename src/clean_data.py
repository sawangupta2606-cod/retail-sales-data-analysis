
import pandas as pd
from pathlib import Path

# File locations
input_file = Path("data/raw/Online Retail.xlsx")
output_file = Path("data/processed/retail_cleaned.csv")

print("Loading original dataset...")
df = pd.read_excel(input_file)

original_rows = len(df)

# 1. Remove exact duplicate records
duplicate_count = df.duplicated().sum()
df = df.drop_duplicates().copy()

# 2. Clean text columns
df["InvoiceNo"] = df["InvoiceNo"].astype(str).str.strip()
df["StockCode"] = df["StockCode"].astype(str).str.strip()
df["Description"] = df["Description"].astype("string").str.strip()
df["Country"] = df["Country"].astype("string").str.strip()

# 3. Ensure correct data types
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")

# 4. Create useful transaction flags
df["IsCancelled"] = df["InvoiceNo"].str.startswith("C", na=False)
df["IsReturn"] = df["Quantity"] < 0

# 5. Calculate line revenue
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# 6. Save the cleaned dataset
output_file.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_file, index=False)

print("\n========== CLEANING SUMMARY ==========")
print("Original rows:", original_rows)
print("Duplicate rows removed:", duplicate_count)
print("Rows after duplicate removal:", len(df))
print("Missing customer IDs retained:", df["CustomerID"].isna().sum())
print("Cancelled invoice rows flagged:", df["IsCancelled"].sum())
print("Negative-quantity rows flagged:", df["IsReturn"].sum())
print("Negative-price rows retained:", (df["UnitPrice"] < 0).sum())
print("Missing descriptions retained:", df["Description"].isna().sum())
print("Output file:", output_file)
print("\nData cleaning completed!")
