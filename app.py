import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="TCX3901 - Electronics Order Value Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("electronics_orders.csv")
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    return df

df = load_data()

st.title("Order Value Prediction - Electronics Segment")
st.caption(
    "TCX3901 Industrial Practice | Report 1 EDA dashboard | "
    "Olist Brazilian E-Commerce dataset, electronics + computers_accessories + "
    "computers + tablets_printing_image, delivered orders only (n = 9,297)"
)

# ---------- Sidebar filters (link all views together) ----------
st.sidebar.header("Filters")
states = sorted(df["customer_state"].dropna().unique().tolist())
selected_states = st.sidebar.multiselect("Customer state", states, default=states)

cats = sorted(df["dominant_category"].dropna().unique().tolist())
selected_cats = st.sidebar.multiselect("Dominant category", cats, default=cats)

value_range = st.sidebar.slider(
    "Order value range (R$)",
    float(df["order_value"].min()), float(min(df["order_value"].max(), 1000)),
    (float(df["order_value"].min()), float(min(df["order_value"].max(), 1000)))
)

filtered = df[
    df["customer_state"].isin(selected_states) &
    df["dominant_category"].isin(selected_cats) &
    df["order_value"].between(value_range[0], value_range[1])
]

st.sidebar.markdown(f"**{len(filtered):,}** orders match current filters")

# ---------- Top-level KPIs ----------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Orders", f"{len(filtered):,}")
col2.metric("Mean order value", f"R${filtered['order_value'].mean():.2f}" if len(filtered) else "-")
col3.metric("Median order value", f"R${filtered['order_value'].median():.2f}" if len(filtered) else "-")
col4.metric("High-value share", f"{filtered['high_value'].mean()*100:.1f}%" if len(filtered) else "-")

st.divider()

# ---------- View 1: Order value distribution ----------
st.subheader("1. Order Value Distribution")
threshold = df["order_value"].quantile(0.8)
fig1 = px.histogram(
    filtered, x="order_value", nbins=50,
    labels={"order_value": "Order value (R$)"},
    title="Distribution of order value (80th percentile threshold shown)"
)
fig1.add_vline(x=threshold, line_dash="dash", line_color="red",
                annotation_text=f"80th pct = R${threshold:.2f}")
st.plotly_chart(fig1, use_container_width=True)

col_a, col_b = st.columns(2)

# ---------- View 2: Value by item count ----------
with col_a:
    st.subheader("2. Value by Basket Size")
    item_stats = filtered.groupby("n_items")["order_value"].median().reset_index()
    item_stats = item_stats[item_stats["n_items"] <= 6]
    fig2 = px.bar(
        item_stats, x="n_items", y="order_value",
        labels={"n_items": "Items per order", "order_value": "Median order value (R$)"},
        title="Median order value rises with basket size"
    )
    st.plotly_chart(fig2, use_container_width=True)

# ---------- View 3: Orders by state ----------
with col_b:
    st.subheader("3. Orders by State")
    state_counts = filtered["customer_state"].value_counts().head(10).reset_index()
    state_counts.columns = ["state", "orders"]
    fig3 = px.bar(
        state_counts.sort_values("orders"), x="orders", y="state", orientation="h",
        labels={"orders": "Number of orders", "state": "Customer state"},
        title="Top 10 states by order count"
    )
    st.plotly_chart(fig3, use_container_width=True)

# ---------- View 4: Installments vs value ----------
st.subheader("4. Payment Instalments vs Order Value")
sample = filtered.sample(min(2000, len(filtered)), random_state=42) if len(filtered) > 0 else filtered
fig4 = px.scatter(
    sample, x="payment_installments", y="order_value",
    color="high_value",
    labels={"payment_installments": "Payment instalments", "order_value": "Order value (R$)",
            "high_value": "High-value"},
    title="Higher-value orders tend to use more instalments",
    opacity=0.5
)
st.plotly_chart(fig4, use_container_width=True)

st.divider()
st.caption(
    "Data: Olist Brazilian E-Commerce Public Dataset (Kaggle). "
    "Segment definition, baseline, and prediction-point methodology documented in Report 1, Sections 1, 3, and 5."
)
