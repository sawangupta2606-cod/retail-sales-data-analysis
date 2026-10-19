
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="Retail Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Retail Sales Analysis Dashboard")
st.caption("Explore sales trends, products, and customer performance.")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    file_path = Path("data/processed/retail_cleaned.csv")
    df = pd.read_csv(file_path, parse_dates=["InvoiceDate"])

    df["IsCancelled"] = (
        df["IsCancelled"].astype(str).str.lower() == "true"
    )

    df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Dataset not found. Run src/clean_data.py first.")
    st.stop()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("Dashboard Filters")

countries = sorted(df["Country"].dropna().unique().tolist())
selected_countries = st.sidebar.multiselect(
    "Select countries",
    countries,
    default=["United Kingdom"] if "United Kingdom" in countries else countries
)

min_date = df["InvoiceDate"].min().date()
max_date = df["InvoiceDate"].max().date()

date_range = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) != 2:
    st.info("Select both a start date and an end date.")
    st.stop()

start_date, end_date = date_range

if start_date > end_date:
    st.error("Start date must be before end date.")
    st.stop()

# ---------------- FILTER SALES ----------------
sales = df[
    (~df["IsCancelled"])
    & (df["Quantity"] > 0)
    & (df["UnitPrice"] >= 0)
    & (df["Country"].isin(selected_countries))
    & (df["InvoiceDate"].dt.date >= start_date)
    & (df["InvoiceDate"].dt.date <= end_date)
].copy()

# ---------------- KPI METRICS ----------------
total_revenue = sales["Revenue"].sum()
total_invoices = sales["InvoiceNo"].nunique()
total_items = sales["Quantity"].sum()
total_customers = sales["CustomerID"].nunique()

average_order_value = (
    sales.groupby("InvoiceNo")["Revenue"].sum().mean()
    if not sales.empty else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"£{total_revenue:,.2f}")
col2.metric("Invoices", f"{total_invoices:,}")
col3.metric("Items Sold", f"{total_items:,}")
col4.metric("Customers", f"{total_customers:,}")

st.metric("Average Order Value", f"£{average_order_value:,.2f}")

st.divider()

if sales.empty:
    st.warning("No sales match these filters. Try another country or date range.")
    st.stop()

# ---------------- MONTHLY SALES TREND ----------------
st.subheader("📈 Monthly Sales Trend")

sales["Month"] = sales["InvoiceDate"].dt.to_period("M").astype(str)

monthly_sales = (
    sales.groupby("Month", as_index=False)["Revenue"]
    .sum()
)

fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(
    monthly_sales["Month"],
    monthly_sales["Revenue"],
    marker="o"
)
ax.set_xlabel("Month")
ax.set_ylabel("Revenue (£)")
ax.tick_params(axis="x", rotation=45)
ax.grid(True, linestyle="--", alpha=0.4)
fig.tight_layout()

st.pyplot(fig)
plt.close(fig)

# ---------------- PRODUCT AND COUNTRY ANALYSIS ----------------
left, right = st.columns(2)

with left:
    st.subheader("🏆 Top 10 Products")

    top_products = (
        sales.groupby("Description")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    top_products.plot(kind="barh", ax=ax)
    ax.set_xlabel("Revenue (£)")
    ax.set_ylabel("")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with right:
    st.subheader("🌍 Revenue by Country")

    top_countries = (
        sales.groupby("Country")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    top_countries.plot(kind="barh", ax=ax)
    ax.set_xlabel("Revenue (£)")
    ax.set_ylabel("")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# ---------------- CUSTOMER ANALYSIS ----------------
st.subheader("👥 Customer Performance")

customer_sales = sales.dropna(subset=["CustomerID"]).copy()

customer_summary = (
    customer_sales.groupby("CustomerID")
    .agg(
        TotalRevenue=("Revenue", "sum"),
        TotalInvoices=("InvoiceNo", "nunique")
    )
    .sort_values("TotalRevenue", ascending=False)
)

st.dataframe(customer_summary.head(10).reset_index(), width="stretch", hide_index=True)

# ---------------- RAW DATA PREVIEW ----------------
with st.expander("View filtered transaction data"):
    st.dataframe(sales.head(1000), width="stretch", hide_index=True)

st.caption(
    "Note: Revenue is calculated from positive-quantity, non-cancelled "
    "invoice lines. Returns are excluded, so this is not net revenue."
)
