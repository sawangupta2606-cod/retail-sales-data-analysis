
import pandas as pd
from pathlib import Path

file_path = Path("data/processed/retail_cleaned.csv")

print("Loading cleaned dataset...")
df = pd.read_csv(file_path)

# Keep eligible sales transactions
sales = df[
    (~df["IsCancelled"].astype(bool))
    & (df["Quantity"] > 0)
    & (df["UnitPrice"] >= 0)
].copy()

sales["Revenue"] = sales["Quantity"] * sales["UnitPrice"]

# Top 10 products by revenue
top_products = (
    sales.groupby("Description", dropna=True)["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

# Top 10 countries by revenue
top_countries = (
    sales.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

print("\n========== TOP 10 PRODUCTS ==========")
print(top_products.to_string(index=False))

print("\n========== TOP 10 COUNTRIES ==========")
print(top_countries.to_string(index=False))

# Save reports
output_dir = Path("outputs/reports")
output_dir.mkdir(parents=True, exist_ok=True)

top_products.to_csv(output_dir / "top_products.csv", index=False)
top_countries.to_csv(output_dir / "top_countries.csv", index=False)

print("\nReports saved in outputs/reports/")
