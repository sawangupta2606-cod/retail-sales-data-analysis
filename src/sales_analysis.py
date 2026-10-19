
import pandas as pd
from pathlib import Path

file_path = Path("data/processed/retail_cleaned.csv")

print("Loading cleaned dataset...")
df = pd.read_csv(file_path, parse_dates=["InvoiceDate"])

# Keep completed sales invoices with positive quantities
# and non-negative unit prices.
sales = df[
    (~df["IsCancelled"].astype(bool))
    & (df["Quantity"] > 0)
    & (df["UnitPrice"] >= 0)
].copy()

# Calculate revenue for eligible sales lines
sales["Revenue"] = sales["Quantity"] * sales["UnitPrice"]

# Group sales by month
sales["Month"] = sales["InvoiceDate"].dt.to_period("M")

monthly_sales = (
    sales.groupby("Month", observed=True)["Revenue"]
    .sum()
    .reset_index()
)

monthly_sales["Month"] = monthly_sales["Month"].astype(str)

print("\n========== MONTHLY SALES ==========")
print(monthly_sales.to_string(index=False))

print("\n========== KEY METRICS ==========")
print("Eligible sales lines:", len(sales))
print("Total revenue:", round(sales["Revenue"].sum(), 2))
print("Unique invoices:", sales["InvoiceNo"].nunique())
print("Unique customers:", sales["CustomerID"].nunique())

# Save monthly results
output_file = Path("outputs/reports/monthly_sales.csv")
output_file.parent.mkdir(parents=True, exist_ok=True)
monthly_sales.to_csv(output_file, index=False)

print("\nMonthly report saved to:", output_file)


import matplotlib.pyplot as plt

# Convert month labels and revenue into chart data
months = pd.to_datetime(monthly_sales["Month"])
revenue = monthly_sales["Revenue"]

# Create the chart
plt.figure(figsize=(12, 6))
plt.plot(months, revenue, marker="o", linewidth=2)

plt.title("Monthly Retail Sales Revenue (2010–2011)")
plt.xlabel("Month")
plt.ylabel("Revenue (GBP)")
plt.xticks(rotation=45)
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()

# Save the chart
chart_path = Path("outputs/figures/monthly_sales_trend.png")
chart_path.parent.mkdir(parents=True, exist_ok=True)

plt.savefig(chart_path, dpi=300, bbox_inches="tight")
print("Chart saved to:", chart_path)

plt.show()
