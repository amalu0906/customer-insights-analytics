# Power BI DAX Measures

Use these measures after loading the exported CSV files from `data/processed/`.

## Core Measures

```DAX
Total Revenue = SUM(clean_transactions[revenue])
```

```DAX
Total Orders = DISTINCTCOUNT(clean_transactions[invoiceno])
```

```DAX
Total Customers = DISTINCTCOUNT(clean_transactions[customerid])
```

```DAX
Average Order Value = DIVIDE([Total Revenue], [Total Orders])
```

```DAX
Revenue per Customer = DIVIDE([Total Revenue], [Total Customers])
```

## Customer Segmentation Measures

```DAX
Customers by Segment = DISTINCTCOUNT(customer_rfm_segments[customerid])
```

```DAX
Segment Revenue = SUM(customer_rfm_segments[monetary])
```

```DAX
Segment Revenue Share % =
DIVIDE(
    [Segment Revenue],
    CALCULATE([Segment Revenue], ALL(customer_rfm_segments[customer_segment]))
)
```

## Churn Measures

```DAX
At Risk Customers =
CALCULATE(
    DISTINCTCOUNT(customer_churn_risk[customerid]),
    customer_churn_risk[churn_status] = "At Risk"
)
```

```DAX
Lost Customers =
CALCULATE(
    DISTINCTCOUNT(customer_churn_risk[customerid]),
    customer_churn_risk[churn_status] = "Lost"
)
```

```DAX
Churn Risk Rate =
DIVIDE(
    [At Risk Customers] + [Lost Customers],
    DISTINCTCOUNT(customer_churn_risk[customerid])
)
```

