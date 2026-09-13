# TCX3901 Report 1 - EDA Dashboard

Order value prediction, electronics segment, Olist Brazilian E-Commerce dataset.

## What this is

A 4-view exploratory dashboard supporting Report 1 of TCX3901 Industrial Practice
(AY26/27). Shows the order value distribution, basket-size effect, geographic
concentration, and payment-instalment relationship for the electronics segment
(9,297 delivered orders), matching the analysis in Report 1 Sections 3–5.

## Running locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Data

`electronics_orders.csv` is a pre-aggregated extract derived from the Olist
Brazilian E-Commerce Public Dataset (Kaggle: olistbr/brazilian-ecommerce),
filtered to delivered orders in the electronics, computers_accessories,
computers, and tablets_printing_image categories. See Report 1, Section 3
(Data Model) for the full join and aggregation logic.

## Author

Ryan Ang Lin Yi, A0311388A, Group 6
