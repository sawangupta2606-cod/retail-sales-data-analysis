
import pandas as pd
from pathlib import Path

file_path = Path("data/processed/retail_cleaned.csv")

print("Loading cleaned dataset...")
df = pd.read_csv(file_path)

# Keep eligible sales lines
sales = df[
    (~df["IsCancelled"].astype(bool))
    & (df["Quantity"] > 0)
    & (df["UnitPrice"] >= 0)
].copy()

# Customer analysis requires a known CustomerID
sales = sales.dropna(subset=["CustomerID"]).copy()
sales["CustomerID"] = sales["CustomerID"].astype(int)

sales["Revenue"] = sales["Quantity"] * sales["UnitPrice"]

# Summarize each customer's activity
customer_summary = (
    sales.groupby("CustomerID")
    .agg(
        TotalRevenue=("Revenue", "sum"),
        TotalOrders=("InvoiceNo", "nunique"),
        TotalItems=("Quantity", "sum")
    )
    .reset_index()
)

# Identify repeat customers
repeat_customers = customer_summary[
    customer_summary["TotalOrders"] > 1
]

# Average order value: invoice revenue averaged across invoices
invoice_revenue = (
    sales.groupby("InvoiceNo")["Revenue"]
    .sum()
)

average_order_value = invoice_revenue.mean()

print("\n========== CUSTOMER METRICS ==========")
print("Customers analyzed:", len(customer_summary))
print("Repeat customers:", len(repeat_customers))
print(
    "Repeat customer rate (%):",
    round(len(repeat_customers) / len(customer_summary) * 100, 2)
)
print("Average order value:", round(average_order_value, 2))
print("Average revenue per customer:", round(customer_summary["TotalRevenue"].mean(), 2))

print("\n========== TOP 10 CUSTOMERS ==========")
top_customers = customer_summary.sort_values(
    "TotalRevenue", ascending=False
).head(10)

print(top_customers.to_string(index=False))

# Save the report
output_dir = Path("outputs/reports")
output_dir.mkdir(parents=True, exist_ok=True)

customer_summary.sort_values(
    "TotalRevenue", ascending=False
).to_csv(output_dir / "customer_summary.csv", index=False)

top_customers.to_csv(output_dir / "top_customers.csv", index=False)

print("\nCustomer reports saved in outputs/reports/")
