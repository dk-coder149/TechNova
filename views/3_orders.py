import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta



# -----------------------------------------------------------------
# DATA LOADING (WITH FALLBACK)
# -----------------------------------------------------------------
@st.cache_data
def get_orders_data():
    try:
        from queries import load_orders_analytics
        return load_orders_analytics()
    except Exception:
        np.random.seed(102)
        n = 300
        statuses = ["Delivered", "In Transit", "Processing", "Cancelled", "Returned"]
        pay_methods = ["UPI", "Credit Card", "Net Banking", "Cash on Delivery"]
        channels = ["Online Store", "Retail Outlet", "Mobile App"]
        
        start_date = datetime.now() - timedelta(days=90)
        dates = [start_date + timedelta(days=int(i)) for i in np.random.randint(0, 90, size=n)]
        
        df = pd.DataFrame({
            "order_id": [f"ORD-{5000+i}" for i in range(n)],
            "order_date": dates,
            "status": np.random.choice(statuses, size=n, p=[0.6, 0.15, 0.1, 0.1, 0.05]),
            "payment_method": np.random.choice(pay_methods, size=n),
            "sales_channel": np.random.choice(channels, size=n),
            "order_amount": np.random.uniform(500, 25000, size=n).round(2),
            "delivery_days": np.random.randint(1, 7, size=n)
        })
        return df

df_orders = get_orders_data()

# -----------------------------------------------------------------
# HEADER & FILTERS
# -----------------------------------------------------------------
st.title("🛒 Orders & Fulfillment Analytics")
st.markdown("Track order volumes, delivery performance, payment methods, and fulfillment statuses.")

st.sidebar.header("🔍 Order Filters")
all_statuses = list(df_orders["status"].unique())
selected_statuses = st.sidebar.multiselect("Order Status", options=all_statuses, default=all_statuses)

all_channels = list(df_orders["sales_channel"].unique())
selected_channels = st.sidebar.multiselect("Sales Channel", options=all_channels, default=all_channels)

filtered_orders = df_orders[
    (df_orders["status"].isin(selected_statuses)) & 
    (df_orders["sales_channel"].isin(selected_channels))
]

# -----------------------------------------------------------------
# KPIS
# -----------------------------------------------------------------
total_ord = len(filtered_orders)
delivered_ord = len(filtered_orders[filtered_orders["status"] == "Delivered"])
cancelled_ord = len(filtered_orders[filtered_orders["status"] == "Cancelled"])
total_val = filtered_orders["order_amount"].sum()
avg_del_days = filtered_orders["delivery_days"].mean() if total_ord > 0 else 0

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Orders", f"{total_ord:,}")
k2.metric("Delivered Orders", f"{delivered_ord:,}")
k3.metric("Cancellation Rate", f"{(cancelled_ord/total_ord*100) if total_ord>0 else 0:.1f}%")
k4.metric("Avg Order Value", f"₹{(total_val/total_ord) if total_ord>0 else 0:,.2f}")
k5.metric("Avg Delivery Time", f"{avg_del_days:.1f} Days")

st.markdown("---")

# -----------------------------------------------------------------
# CHARTS
# -----------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 Order Status Distribution")
    status_df = filtered_orders.groupby("status")["order_id"].count().reset_index()
    fig_status = px.pie(status_df, names="status", values="order_id", hole=0.4, title="Fulfillment Breakdown")
    st.plotly_chart(fig_status, use_container_width=True)

with col2:
    st.subheader("💳 Preferred Payment Methods")
    pay_df = filtered_orders.groupby("payment_method")["order_amount"].sum().reset_index()
    fig_pay = px.bar(pay_df, x="payment_method", y="order_amount", color="payment_method", labels={"order_amount": "Revenue (₹)"})
    st.plotly_chart(fig_pay, use_container_width=True)

# -----------------------------------------------------------------
# TABLE
# -----------------------------------------------------------------
st.subheader("📋 Detailed Orders List")
st.dataframe(filtered_orders.sort_values("order_date", ascending=False), use_container_width=True, hide_index=True)


#############################################

@st.cache_data(ttl=3600)
def get_order_data():
    try:
        from queries import load_orders_analytics
        df = load_orders_analytics()
        if df.empty: raise ValueError
    except Exception:
        np.random.seed(42)
        n = 300
        statuses = ["Delivered", "Delivered", "Delivered", "Processing", "Cancelled", "Returned"]
        payments = ["Credit Card", "UPI", "Net Banking", "COD"]
        channels = ["Website", "Mobile App", "Store"]
        
        df = pd.DataFrame({
            "order_id": [f"ORD-{10000+i}" for i in range(n)],
            "order_date": pd.date_range(end=pd.Timestamp.now(), periods=n, freq="h"),
            "status": np.random.choice(statuses, size=n),
            "payment_method": np.random.choice(payments, size=n),
            "sales_channel": np.random.choice(channels, size=n),
            "order_amount": np.random.uniform(300, 15000, size=n).round(2),
            "delivery_days": np.random.randint(1, 7, size=n)
        })
    return df

df_orders = get_order_data()

# Order Filters
st.sidebar.header("🎯 Order Filters")
selected_status = st.sidebar.multiselect("Status Filter", df_orders["status"].unique(), default=df_orders["status"].unique())
selected_channel = st.sidebar.multiselect("Channel Filter", df_orders["sales_channel"].unique(), default=df_orders["sales_channel"].unique())

filtered_orders = df_orders[
    (df_orders["status"].isin(selected_status)) & 
    (df_orders["sales_channel"].isin(selected_channel))
]

# Metrics
m1, m2, m3, m4 = st.columns(4)
total_count = len(filtered_orders)
m1.metric("Total Orders", f"{total_count:,}")
m2.metric("Delivered Orders", f"{len(filtered_orders[filtered_orders['status'] == 'Delivered']):,}")
m3.metric("Cancelled Rate", f"{(len(filtered_orders[filtered_orders['status'] == 'Cancelled']) / max(total_count, 1) * 100):.1f}%")
m4.metric("Return Rate", f"{(len(filtered_orders[filtered_orders['status'] == 'Returned']) / max(total_count, 1) * 100):.1f}%")

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📜 Order History & Details", "📊 Order Status & Channels", "⚠️ Returns & Cancellations"])

with tab1:
    st.subheader("Order Log")
    st.dataframe(filtered_orders, use_container_width=True, hide_index=True)

with tab2:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Order Status Distribution")
        fig_status = px.pie(filtered_orders, names="status", title="Status Breakdown", hole=0.4)
        st.plotly_chart(fig_status, use_container_width=True)
    with c2:
        st.subheader("Sales Channel Split")
        fig_chan = px.bar(filtered_orders.groupby("sales_channel")["order_amount"].sum().reset_index(),
                          x="sales_channel", y="order_amount", color="sales_channel", title="Revenue by Channel")
        st.plotly_chart(fig_chan, use_container_width=True)

with tab3:
    st.subheader("Cancelled & Returned Orders Deep Dive")
    bad_orders = filtered_orders[filtered_orders["status"].isin(["Cancelled", "Returned"])]
    if bad_orders.empty:
        st.info("No cancelled or returned orders found for current selection.")
    else:
        fig_bad = px.histogram(bad_orders, x="payment_method", color="status", barmode="group",
                              title="Cancellations & Returns by Payment Method")
        st.plotly_chart(fig_bad, use_container_width=True)
        st.dataframe(bad_orders, use_container_width=True)