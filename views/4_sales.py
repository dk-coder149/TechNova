import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px



# -----------------------------------------------------------------
# DATA LOADING (WITH FALLBACK)
# -----------------------------------------------------------------
@st.cache_data
def get_sales_data():
    try:
        from queries import load_sales_analytics
        return load_sales_analytics()
    except Exception:
        np.random.seed(103)
        months = pd.date_range(start="2025-01-01", periods=12, freq="ME").strftime("%b %Y")
        
        df = pd.DataFrame({
            "month": months,
            "gross_sales": np.random.uniform(500000, 1500000, size=12).round(2),
            "discounts": np.random.uniform(20000, 80000, size=12).round(2),
            "returns": np.random.uniform(10000, 50000, size=12).round(2),
            "target": np.random.uniform(600000, 1400000, size=12).round(2)
        })
        df["net_sales"] = df["gross_sales"] - df["discounts"] - df["returns"]
        return df

df_sales = get_sales_data()

# -----------------------------------------------------------------
# HEADER & KPIS
# -----------------------------------------------------------------
st.title("📈 Comprehensive Sales Analytics")
st.markdown("Revenue streams, discount impact, net sales performance, and target achievement.")

total_gross = df_sales["gross_sales"].sum()
total_discounts = df_sales["discounts"].sum()
total_net = df_sales["net_sales"].sum()
total_target = df_sales["target"].sum()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Gross Revenue", f"₹{total_gross/1e5:.2f} L")
k2.metric("Total Discounts", f"₹{total_discounts/1e5:.2f} L")
k3.metric("Net Sales", f"₹{total_net/1e5:.2f} L")
k4.metric("Target Achievement", f"{(total_net/total_target*100):.1f}%")

st.markdown("---")

# -----------------------------------------------------------------
# CHARTS
# -----------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Monthly Sales Performance vs Target")
    fig_sales = px.bar(df_sales, x="month", y=["net_sales", "target"], barmode="group", labels={"value": "Amount (₹)"})
    st.plotly_chart(fig_sales, use_container_width=True)

with col2:
    st.subheader("📉 Discount & Return Impact")
    fig_impact = px.line(df_sales, x="month", y=["discounts", "returns"], markers=True)
    st.plotly_chart(fig_impact, use_container_width=True)

st.subheader("📋 Monthly Sales Ledger")
st.dataframe(df_sales, use_container_width=True, hide_index=True)





########################################



@st.cache_data(ttl=3600)
def get_sales_data():
    try:
        from queries import load_sales_analytics
        df = load_sales_analytics()
        if df.empty: raise ValueError
    except Exception:
        np.random.seed(42)
        dates = pd.date_range(start="2025-01-01", end="2026-08-01", freq="D")
        states = ["Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "Gujarat", "Uttar Pradesh"]
        categories = ["Electronics", "Fashion", "Home", "Beauty"]
        
        n = len(dates)
        df = pd.DataFrame({
            "date": dates,
            "gross_sales": np.random.uniform(10000, 80000, size=n).round(2),
            "discounts": np.random.uniform(500, 5000, size=n).round(2),
            "returns": np.random.uniform(200, 3000, size=n).round(2),
            "state": np.random.choice(states, size=n),
            "category": np.random.choice(categories, size=n)
        })
        df["net_sales"] = df["gross_sales"] - df["discounts"] - df["returns"]
    return df

df_sales = get_sales_data()

# Date Range & Granularity Controls
c1, c2, c3 = st.columns([2, 1, 1])
with c1:
    date_range = st.date_input("🗓️ Select Date Range", [df_sales["date"].min(), df_sales["date"].max()])
with c2:
    granularity = st.selectbox("⏱️ Time Granularity", ["Daily", "Weekly", "Monthly", "Yearly"])

# Filter by Date Range
start_d, end_d = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
filtered_sales = df_sales[(df_sales["date"] >= start_d) & (df_sales["date"] <= end_d)].copy()

# Apply Granularity Aggregation
if granularity == "Weekly":
    filtered_sales["period"] = filtered_sales["date"].dt.to_period("W").dt.start_time
elif granularity == "Monthly":
    filtered_sales["period"] = filtered_sales["date"].dt.to_period("M").dt.start_time
elif granularity == "Yearly":
    filtered_sales["period"] = filtered_sales["date"].dt.to_period("Y").dt.start_time
else:
    filtered_sales["period"] = filtered_sales["date"]

trend_df = filtered_sales.groupby("period")["net_sales"].sum().reset_index()

# KPIs
k1, k2, k3, k4 = st.columns(4)
k1.metric("Gross Sales", f"₹{filtered_sales['gross_sales'].sum():,.2f}")
k2.metric("Total Discounts", f"₹{filtered_sales['discounts'].sum():,.2f}")
k3.metric("Total Returns", f"₹{filtered_sales['returns'].sum():,.2f}")
k4.metric("Net Revenue", f"₹{filtered_sales['net_sales'].sum():,.2f}")

st.markdown("---")

st.subheader(f"📊 Revenue Trend ({granularity} View)")
fig_trend = px.line(trend_df, x="period", y="net_sales", markers=True, title="Net Revenue Over Time")
st.plotly_chart(fig_trend, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.subheader("State-wise Sales Distribution")
    state_df = filtered_sales.groupby("state")["net_sales"].sum().reset_index()
    fig_state = px.bar(state_df, x="state", y="net_sales", color="state", title="Net Sales by State")
    st.plotly_chart(fig_state, use_container_width=True)

with col2:
    st.subheader("Category-wise Revenue Contribution")
    cat_df = filtered_sales.groupby("category")["net_sales"].sum().reset_index()
    fig_cat = px.pie(cat_df, values="net_sales", names="category", title="Category Sales Breakdown", hole=0.3)
    st.plotly_chart(fig_cat, use_container_width=True)