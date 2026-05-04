# 🧠 Customer Insights & Revenue Performance Dashboard

An end-to-end analytics project that transforms transactional retail data into actionable customer insights using data modelling, segmentation, and visualisation.

---

## 📸 Dashboard Preview

![Dashboard Overview](images/dashboard_overview.png)

---

## 🎯 Objective

To build a customer insights dashboard that:

* Tracks revenue performance over time
* Identifies high-value customer segments
* Analyses customer retention and churn risk
* Supports data-driven business decisions

---

## 📊 Dataset

* **Source:** UCI Online Retail Dataset (UK-based e-commerce transactions)
* **Period:** 2010–2011
* **Data Includes:**

  * Customer transactions
  * Order-level data
  * Revenue metrics

---

## 🛠️ Tools & Technologies

* **Python (Pandas):** Data cleaning and transformation
* **Power BI:** Data modelling and dashboard development
* **SQL:** Reference queries for transformation logic

---

## 📁 Project Structure

```text
├── data/
│   └── processed/              # Cleaned datasets used in Power BI
│
├── images/                     # Dashboard screenshots
│   ├── dashboard_overview.png
│   ├── revenue_trend.png
│   ├── customer_segments.png
│   ├── churn_analysis.png
│   └── top_customers.png
│
├── powerbi/
│   ├── customer_insights_dashboard.pbix
│   ├── powerbi_measures.md
│   ├── data_model.png
│   ├── wireframe.png
│   └── powerbi_notes.md
│
├── sql/                        # Optional SQL logic
│   ├── data_cleaning.sql
│   ├── monthly_summary.sql
│   └── rfm_segmentation.sql
│
├── insights_summary.md
└── README.md
```

---

## 📊 Dashboard Overview

### 🔹 KPI Cards

* Total Revenue
* Total Orders
* Total Customers
* Average Order Value

👉 Provides a high-level snapshot of business performance

---

### 📈 Revenue Trend

* Monthly revenue analysis

👉 Identifies patterns, trends, and potential seasonality

---

### 📊 Customer Segmentation

* Revenue contribution by segment

👉 Highlights which customer groups drive the most revenue

---

### 🍩 Customer Retention (Churn Analysis)

* Active vs At Risk vs Lost customers

👉 Helps prioritise retention strategies

---

### 📋 Top Customers

* High-value customers based on revenue

👉 Supports targeted engagement and marketing

---

### 🎛️ Filters

* Country
* Customer Segment

👉 Enables dynamic exploration of the data

---

## 🧠 Key Insights

* A small group of high-value customer segments contributes a significant share of total revenue
* A notable portion of customers fall into “At Risk” and “Lost” categories
* Revenue trends show variability across months, suggesting changes in customer behaviour

---

## 💡 Business Impact

* Focus retention efforts on high-value customers to protect revenue
* Target “At Risk” customers with timely engagement strategies
* Use segmentation to personalise marketing and improve conversion
* Monitor trends to support planning and forecasting

---

## 🧱 Dashboard Design Approach

![Wireframe](powerbi/wireframe.png)

Designed using a top-down approach:

**KPIs → Trends → Segmentation → Retention**

---

## ⚙️ Data Model

![Data Model](powerbi/data_model.png)

* Multiple structured datasets used for performance optimisation
* Pre-aggregated tables used for trend and segmentation analysis
* Separate churn summary table created to ensure accurate aggregation

---

## 🧾 Power BI Logic

See:

```text
powerbi/powerbi_measures.md
```

---

## 🗣️ How to Explain This Project (Interview)

This project demonstrates the ability to:

* Transform raw transactional data into structured datasets
* Build customer segmentation and churn logic
* Design a clear and business-focused dashboard
* Communicate insights effectively to stakeholders

---

## 🚀 Conclusion

This project showcases a practical approach to customer analytics by combining data preparation, segmentation, and visualisation to support business decision-making.
