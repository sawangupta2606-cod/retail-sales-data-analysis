
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

report_dir = Path("outputs/reports")
figure_dir = Path("outputs/figures")
figure_dir.mkdir(parents=True, exist_ok=True)

# Load existing reports
products = pd.read_csv(report_dir / "top_products.csv")
countries = pd.read_csv(report_dir / "top_countries.csv")

# Chart 1: Top products by revenue
products = products.sort_values("Revenue")

plt.figure(figsize=(12, 7))
plt.barh(products["Description"], products["Revenue"])
plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue (GBP)")
plt.ylabel("Product")
plt.tight_layout()
plt.savefig(
    figure_dir / "top_products.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()
plt.close()

# Chart 2: Top countries by revenue
countries = countries.sort_values("Revenue")

plt.figure(figsize=(10, 6))
plt.barh(countries["Country"], countries["Revenue"])
plt.title("Top 10 Countries by Revenue")
plt.xlabel("Revenue (GBP)")
plt.ylabel("Country")
plt.tight_layout()
plt.savefig(
    figure_dir / "top_countries.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()
plt.close()

print("Both charts saved successfully!")
print("Location: outputs/figures/")
