"""
Customer Insights & Retention Analytics Portfolio Project

This script:
1. Loads the UCI Online Retail dataset
2. Cleans transaction records
3. Builds RFM customer segmentation
4. Identifies churn risk
5. Exports clean CSV files for Power BI
"""

import pandas as pd
import numpy as np
from config import RAW_FILE, PROCESSED_DIR


def load_data() -> pd.DataFrame:
    """Load raw Online Retail dataset."""
    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {RAW_FILE}\n"
            "Download 'Online Retail.xlsx' from UCI and place it in the data folder."
        )

    df = pd.read_excel(RAW_FILE)
    return df


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Clean cancelled, missing and invalid transaction records."""
    df = df.copy()

    # Standardise column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Remove missing customer IDs
    df = df[df["customerid"].notna()]

    # Remove cancelled invoices
    df = df[~df["invoiceno"].astype(str).str.startswith("C")]

    # Remove invalid quantities and prices
    df = df[(df["quantity"] > 0) & (df["unitprice"] > 0)]

    # Convert data types
    df["customerid"] = df["customerid"].astype(int).astype(str)
    df["invoicedate"] = pd.to_datetime(df["invoicedate"])

    # Create commercial metrics
    df["revenue"] = df["quantity"] * df["unitprice"]
    df["invoice_month"] = df["invoicedate"].dt.to_period("M").astype(str)

    return df


def build_rfm(df: pd.DataFrame) -> pd.DataFrame:
    """Create customer-level RFM table and business-friendly segments."""
    analysis_date = df["invoicedate"].max() + pd.Timedelta(days=1)

    rfm = (
        df.groupby("customerid")
        .agg(
            recency=("invoicedate", lambda x: (analysis_date - x.max()).days),
            frequency=("invoiceno", "nunique"),
            monetary=("revenue", "sum"),
            first_purchase=("invoicedate", "min"),
            last_purchase=("invoicedate", "max"),
            total_items=("quantity", "sum"),
        )
        .reset_index()
    )

    # RFM scores: 5 is best
    rfm["r_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1], duplicates="drop")
    rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5], duplicates="drop")
    rfm["m_score"] = pd.qcut(rfm["monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5], duplicates="drop")

    rfm[["r_score", "f_score", "m_score"]] = rfm[["r_score", "f_score", "m_score"]].astype(int)
    rfm["rfm_score"] = rfm["r_score"] + rfm["f_score"] + rfm["m_score"]

    def assign_segment(row):
        if row["r_score"] >= 4 and row["f_score"] >= 4 and row["m_score"] >= 4:
            return "Champions"
        if row["r_score"] >= 3 and row["f_score"] >= 4:
            return "Loyal Customers"
        if row["r_score"] >= 4 and row["f_score"] <= 3:
            return "Potential Loyalists"
        if row["r_score"] <= 2 and row["f_score"] >= 3:
            return "At Risk"
        if row["r_score"] <= 2 and row["f_score"] <= 2:
            return "Lost Customers"
        return "Needs Attention"

    rfm["customer_segment"] = rfm.apply(assign_segment, axis=1)

    return rfm


def build_churn_table(rfm: pd.DataFrame) -> pd.DataFrame:
    """Classify customers by inactivity risk."""
    churn = rfm.copy()

    def churn_status(recency):
        if recency <= 90:
            return "Active"
        if recency <= 180:
            return "At Risk"
        return "Lost"

    churn["churn_status"] = churn["recency"].apply(churn_status)

    return churn[
        [
            "customerid",
            "recency",
            "frequency",
            "monetary",
            "customer_segment",
            "churn_status",
            "first_purchase",
            "last_purchase",
        ]
    ]


def build_monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Create monthly performance summary for dashboarding."""
    monthly = (
        df.groupby("invoice_month")
        .agg(
            total_revenue=("revenue", "sum"),
            total_orders=("invoiceno", "nunique"),
            total_customers=("customerid", "nunique"),
            total_items=("quantity", "sum"),
        )
        .reset_index()
    )

    monthly["average_order_value"] = monthly["total_revenue"] / monthly["total_orders"]
    monthly["revenue_per_customer"] = monthly["total_revenue"] / monthly["total_customers"]

    return monthly


def build_segment_summary(rfm: pd.DataFrame) -> pd.DataFrame:
    """Summarise value and behaviour by customer segment."""
    segment_summary = (
        rfm.groupby("customer_segment")
        .agg(
            customers=("customerid", "count"),
            avg_recency=("recency", "mean"),
            avg_frequency=("frequency", "mean"),
            total_revenue=("monetary", "sum"),
            avg_customer_value=("monetary", "mean"),
        )
        .reset_index()
        .sort_values("total_revenue", ascending=False)
    )

    total_revenue = segment_summary["total_revenue"].sum()
    segment_summary["revenue_share_pct"] = (
        segment_summary["total_revenue"] / total_revenue * 100
    ).round(2)

    return segment_summary


def main():
    raw = load_data()
    clean = clean_transactions(raw)

    rfm = build_rfm(clean)
    churn = build_churn_table(rfm)
    monthly = build_monthly_summary(clean)
    segment_summary = build_segment_summary(rfm)

    clean.to_csv(PROCESSED_DIR / "clean_transactions.csv", index=False)
    rfm.to_csv(PROCESSED_DIR / "customer_rfm_segments.csv", index=False)
    churn.to_csv(PROCESSED_DIR / "customer_churn_risk.csv", index=False)
    monthly.to_csv(PROCESSED_DIR / "monthly_performance_summary.csv", index=False)
    segment_summary.to_csv(PROCESSED_DIR / "segment_summary.csv", index=False)

    print("Customer insights outputs created successfully.")
    print(f"Files saved to: {PROCESSED_DIR}")


if __name__ == "__main__":
    main()
