import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px




# -----------------------------------------------------------------
# DATA LOADING (WITH FALLBACK)
# -----------------------------------------------------------------
@st.cache_data
def get_inventory_data():
    try:
        from queries import load_inventory_analytics
        return load_inventory_analytics()
    except Exception:
        np.random.seed(105)
        n = 50
        categories = ["Electronics", "Clothing", "Home & Kitchen", "Books", "Beauty"]
        
        df = pd.DataFrame({
            "sku_id": [f"SKU-{3000+i}" for i in range(n)],
            "item_name": [f"Stock Item {i+1}" for i in range(n)],
            "category": np.random.choice(categories, size=n),
            "current_stock": np.random.randint(0, 150, size=n),
            "reorder_level": np.random.randint(20, 40, size=n),
            "unit_cost": np.random.uniform(100, 5000, size=n).round(2)
        })
        df["stock_value"] = (df["current_stock"] * df["unit_cost"]).round(2)
        df["reorder_status"] = np.where(df["current_stock"] <= df["reorder_level"], "Reorder Needed", "Sufficient")
        return df

df_inv = get_inventory_data()

# -----------------------------------------------------------------
# HEADER & KPIS
# -----------------------------------------------------------------
st.title("📋 Inventory & Stock Health Analytics")
st.markdown("Real-time stock level monitoring, valuation, and automated reorder alerts.")

total_skus = len(df_inv)
total_valuation = df_inv["stock_value"].sum()
reorder_count = len(df_inv[df_inv["reorder_status"] == "Reorder Needed"])
out_of_stock = len(df_inv[df_inv["current_stock"] == 0])

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total SKUs Managed", f"{total_skus}")
k2.metric("Total Stock Valuation", f"₹{total_valuation/1e5:.2f} L")
k3.metric("Reorder Alerts", f"{reorder_count}", delta="-Action Req" if reorder_count>0 else "OK", delta_color="inverse")
k4.metric("Out of Stock Items", f"{out_of_stock}", delta="-Critical" if out_of_stock>0 else "OK", delta_color="inverse")

st.markdown("---")

# -----------------------------------------------------------------
# CHARTS
# -----------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 Stock Value Distribution by Category")
    val_df = df_inv.groupby("category")["stock_value"].sum().reset_index()
    fig_val = px.bar(val_df, x="category", y="stock_value", color="category", labels={"stock_value": "Valuation (₹)"})
    st.plotly_chart(fig_val, use_container_width=True)

with col2:
    st.subheader("⚠️ Stock Status Ratio")
    status_df = df_inv["reorder_status"].value_counts().reset_index()
    status_df.columns = ["Status", "Count"]
    fig_status = px.pie(status_df, names="Status", values="Count", hole=0.4, color_discrete_sequence=["#EF4444", "#10B981"])
    st.plotly_chart(fig_status, use_container_width=True)

st.subheader("📋 Stock Audit & Reorder Warning Table")
st.dataframe(df_inv.sort_values("current_stock", ascending=True), use_container_width=True, hide_index=True)




#######################################



@st.cache_data(ttl=3600)
def get_inventory_data():
    try:
        from queries import load_inventory_analytics
        df = load_inventory_analytics()
        if df.empty: raise ValueError
    except Exception:
        np.random.seed(42)
        categories = ["Electronics", "Clothing", "Home & Kitchen", "Books"]
        n = 80
        stocks = np.random.randint(0, 150, size=n)
        reorder_levels = np.random.randint(10, 30, size=n)
        cost_prices = np.random.uniform(100, 5000, size=n).round(2)
        
        df = pd.DataFrame({
            "sku_id": [f"SKU-{200+i}" for i in range(n)],
            "item_name": [f"Product SKU {i+1}" for i in range(n)],
            "category": np.random.choice(categories, size=n),
            "current_stock": stocks,
            "reorder_level": reorder_levels,
            "unit_cost": cost_prices
        })
        
    df["stock_value"] = (df["current_stock"] * df["unit_cost"]).round(2)
    
    def get_stock_status(row):
        if row["current_stock"] == 0:
            return "Out of Stock"
        elif row["current_stock"] <= row["reorder_level"]:
            return "Low Stock"
        else:
            return "Sufficient"
            
    df["reorder_status"] = df.apply(get_stock_status, axis=1)
    return df

df_inv = get_inventory_data()

# Status Filter
status_filter = st.sidebar.radio("Filter Stock Status", ["All", "Sufficient", "Low Stock", "Out of Stock"])

filtered_inv = df_inv.copy()
if status_filter != "All":
    filtered_inv = filtered_inv[filtered_inv["reorder_status"] == status_filter]

# Metrics
i1, i2, i3, i4 = st.columns(4)
i1.metric("Total Inventory Value", f"₹{df_inv['stock_value'].sum():,.2f}")
i2.metric("Total Items / SKUs", len(df_inv))
i3.metric("Low Stock Warning", len(df_inv[df_inv["reorder_status"] == "Low Stock"]))
i4.metric("Out of Stock Alerts", len(df_inv[df_inv["reorder_status"] == "Out of Stock"]))

st.markdown("---")

tab1, tab2, tab3 = tab1, tab2, tab3 = st.tabs(["📦 Current Stock Catalog", "🚨 Critical Alerts (Low/Out of Stock)", "💰 Valuation & Category Split"])

with tab1:
    st.subheader("Inventory Stock List")
    st.dataframe(filtered_inv, use_container_width=True, hide_index=True)

with tab2:
    st.subheader("Urgent Stock Reorder Action Required")
    alerts = df_inv[df_inv["reorder_status"].isin(["Low Stock", "Out of Stock"])]
    if alerts.empty:
        st.success("All inventory items are currently sufficiently stocked!")
    else:
        st.dataframe(alerts[["sku_id", "item_name", "category", "current_stock", "reorder_level", "reorder_status"]], use_container_width=True)

with tab3:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Stock Value Distribution by Category")
        val_df = df_inv.groupby("category")["stock_value"].sum().reset_index()
        fig_val = px.pie(val_df, values="stock_value", names="category", title="Category Valuation (₹)", hole=0.3)
        st.plotly_chart(fig_val, use_container_width=True)
        
    with c2:
        st.subheader("Stock Level Status Overview")
        status_counts = df_inv["reorder_status"].value_counts().reset_index()
        fig_stat = px.bar(status_counts, x="reorder_status", y="count", color="reorder_status", title="Items per Stock Status Category")
        st.plotly_chart(fig_stat, use_container_width=True)