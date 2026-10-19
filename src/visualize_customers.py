
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

file_path = Path("outputs/reports/top_customers.csv")
df = pd.read_csv(file_path)

# Sort so the largest customer appears at the top
df = df.sort_values("TotalRevenue", ascending=True)

plt.figure(figsize=(10, 7))
plt.barh(
    df["CustomerID"].astype(str),
    df["TotalRevenue"]
)

plt.title("Top 10 Customers by Revenue")
plt.xlabel("Revenue (GBP)")
plt.ylabel("Customer ID")
plt.grid(axis="x", linestyle="--", alpha=0.4)
plt.tight_layout()

output_file = Path("outputs/figures/top_customers.png")
output_file.parent.mkdir(parents=True, exist_ok=True)

plt.savefig(output_file, dpi=300, bbox_inches="tight")
print("Customer chart saved to:", output_file)

plt.show()
