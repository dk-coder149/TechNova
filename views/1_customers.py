from datetime import datetime
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st



# -----------------------------------------------------------------
# 1. HELPER FUNCTION (Data Load with Fallback)
# -----------------------------------------------------------------
@st.cache_data
def get_customer_data():
    try:
        from queries import load_customer_analytics

        return load_customer_analytics()
    except Exception:
        # Fallback Mock Data agar Database Query ready na ho
        np.random.seed(42)
        n = 200
        dates = pd.date_range(start="2025-01-01", periods=n, freq="D")
        segments = ["Champions", "Loyal Customers", "At Risk", "New / Recent"]

        df = pd.DataFrame(
            {
                "customer_id": [f"CUST-{1000+i}" for i in range(n)],
                "customer_name": [
                    f"Customer {i+1}" for i in range(n)
                ],  # Real names default
                "signup_date": np.random.choice(dates, size=n),
                "total_orders": np.random.randint(1, 25, size=n),
                "total_spent": np.random.uniform(500, 150000, size=n).round(2),
                "segment": np.random.choice(
                    segments, size=n, p=[0.2, 0.3, 0.25, 0.25]
                ),
            }
        )
        # Calculate CLV & Repeat Customer flag
        df["clv"] = df["total_spent"] * 1.2
        df["is_repeat"] = df["total_orders"] > 1
        return df


df_cust = get_customer_data()

# -----------------------------------------------------------------
# 2. PAGE HEADER & SIDEBAR FILTERS
# -----------------------------------------------------------------
st.title("👥 Customer Analytics & Insights")
st.markdown("Detailed breakdown of customer acquisition, CLV, and loyalty.")

st.sidebar.header("🔍 Customer Filters")

# Segment Filter
all_segments = list(df_cust["segment"].unique())
selected_segments = st.sidebar.multiselect(
    "Filter by Segment", options=all_segments, default=all_segments
)

# Apply Filter
filtered_df = df_cust[df_cust["segment"].isin(selected_segments)]

# -----------------------------------------------------------------
# 3. TOP KPI CARDS
# -----------------------------------------------------------------
total_cust = len(filtered_df)
repeat_cust_count = filtered_df["is_repeat"].sum()
repeat_rate = (
    (repeat_cust_count / total_cust * 100) if total_cust > 0 else 0
)
avg_clv = filtered_df["clv"].mean() if total_cust > 0 else 0
total_rev = filtered_df["total_spent"].sum()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Customers", f"{total_cust:,}")
kpi2.metric("Repeat Rate", f"{repeat_rate:.1f}%")
kpi3.metric("Avg CLV", f"₹{avg_clv:,.2f}")
kpi4.metric(
    "Customer Lifetime Value (Sum)",
    f"₹{total_rev / 1e5:.2f} L" if total_rev >= 1e5 else f"₹{total_rev:,.2f}",
)

st.markdown("---")

# -----------------------------------------------------------------
# 4. CHARTS: GROWTH, REPEAT & SEGMENTATION
# -----------------------------------------------------------------
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    # FEATURE 3: Customer Growth
    st.subheader("📈 Customer Growth Over Time")
    filtered_df["month"] = (
        pd.to_datetime(filtered_df["signup_date"])
        .dt.to_period("M")
        .astype(str)
    )
    growth_df = (
        filtered_df.groupby("month")["customer_id"].count().reset_index()
    )
    growth_df.rename(columns={"customer_id": "New Customers"}, inplace=True)

    fig_growth = px.line(
        growth_df,
        x="month",
        y="New Customers",
        markers=True,
        title="Monthly New Customer Acquisition",
    )
    st.plotly_chart(fig_growth, use_container_width=True)

with col_chart2:
    # FEATURE 6: Customer Segmentation
    st.subheader("🎯 Customer Segmentation (RFM)")
    seg_df = (
        filtered_df.groupby("segment")["customer_id"].count().reset_index()
    )

    fig_seg = px.pie(
        seg_df,
        names="segment",
        values="customer_id",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Bold,
        title="Customer Distribution by Segment",
    )
    st.plotly_chart(fig_seg, use_container_width=True)

# -----------------------------------------------------------------
# 5. CHARTS: CLV & REPEAT CUSTOMERS
# -----------------------------------------------------------------
col_chart3, col_chart4 = st.columns(2)

with col_chart3:
    # FEATURE 4: Repeat Customers Analysis
    st.subheader("🔄 Repeat vs One-Time Customers")
    repeat_df = (
        filtered_df["is_repeat"]
        .map({True: "Repeat Customer", False: "One-Time Customer"})
        .value_counts()
        .reset_index()
    )
    repeat_df.columns = ["Type", "Count"]

    fig_repeat = px.bar(
        repeat_df,
        x="Type",
        y="Count",
        color="Type",
        text_auto=True,
        title="Order Frequency Ratio",
    )
    st.plotly_chart(fig_repeat, use_container_width=True)

with col_chart4:
    # FEATURE 5: Customer Lifetime Value (CLV)
    st.subheader("💎 Lifetime Value vs Orders")
    fig_clv = px.scatter(
        filtered_df,
        x="total_orders",
        y="clv",
        size="total_spent",
        color="segment",
        hover_name="customer_name",
        title="CLV Correlation with Order Count",
        labels={"total_orders": "Total Orders", "clv": "Estimated CLV (₹)"},
    )
    st.plotly_chart(fig_clv, use_container_width=True)

st.markdown("---")

# -----------------------------------------------------------------
# 6. TABLES: TOP CUSTOMERS & COMPLETE CUSTOMER LIST
# -----------------------------------------------------------------
tab_top, tab_list = st.tabs(["👑 Top Customers (VIPs)", "📋 Full Customer List"])

with tab_top:
    # FEATURE 2: Top Customers
    st.subheader(" Top 10 High-Value Customers")
    top_10 = filtered_df.sort_values(
        by="total_spent", ascending=False
    ).head(10)
    st.dataframe(
        top_10[
            [
                "customer_id",
                "customer_name",
                "segment",
                "total_orders",
                "total_spent",
                "clv",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

with tab_list:
    # FEATURE 1: Searchable Customer List
    st.subheader("🔍 Searchable Customer Directory")
    search_query = st.text_input(
        "Search by Customer Name or ID:", "", placeholder="Type name or ID..."
    )

    if search_query:
        search_filtered = filtered_df[
            filtered_df["customer_name"]
            .str.contains(search_query, case=False, na=False)
            | filtered_df["customer_id"]
            .str.contains(search_query, case=False, na=False)
        ]
    else:
        search_filtered = filtered_df

    st.dataframe(
        search_filtered[
            [
                "customer_id",
                "customer_name",
                "signup_date",
                "segment",
                "total_orders",
                "total_spent",
                "clv",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )
##################################


# Data Loader with Safe Column Fallback & Type Conversion
@st.cache_data(ttl=3600)
def get_customer_data():
    try:
        from queries import load_rfm_data
        df = load_rfm_data()
        if df.empty: raise ValueError
    except Exception:
        np.random.seed(42)
        n = 250
        df = pd.DataFrame({
            "customer_id": [f"CUST-{1000+i}" for i in range(n)],
            "customer_name": [f"Customer {i+1}" for i in range(n)],
            "total_orders": np.random.randint(1, 25, size=n),
            "total_spent": np.random.uniform(500, 150000, size=n).round(2),
            "join_date": pd.date_range(end=pd.Timestamp.now(), periods=n, freq="d"),
            "last_order_days_ago": np.random.randint(1, 180, size=n)
        })
    
    # Ensure ID and Name are always string types
    df["customer_id"] = df["customer_id"].astype(str)
    df["customer_name"] = df["customer_name"].astype(str)

    # Safe checks for missing columns from database SQL query
    if "join_date" not in df.columns:
        df["join_date"] = pd.date_range(end=pd.Timestamp.now(), periods=len(df), freq="d")
    else:
        df["join_date"] = pd.to_datetime(df["join_date"])

    if "last_order_days_ago" not in df.columns:
        df["last_order_days_ago"] = np.random.randint(1, 180, size=len(df))

    # Calculate derived features (CLV, Repeat Rate, Segmentation)
    df["clv"] = (df["total_spent"] * 1.25).round(2)
    df["is_repeat"] = df["total_orders"] > 1
    
    def segment_customer(row):
        spent = row.get("total_spent", 0)
        orders = row.get("total_orders", 0)
        last_days = row.get("last_order_days_ago", 30)

        if spent > 80000 and last_days <= 30:
            return "VIP / High Value"
        elif orders > 5:
            return "Loyal Customer"
        elif last_days > 90:
            return "At Risk / Churning"
        else:
            return "Regular Customer"
            
    df["segment"] = df.apply(segment_customer, axis=1)
    return df

df_cust = get_customer_data()

# KPI Row
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Customers", f"{len(df_cust):,}")
col2.metric("Repeat Customer Rate", f"{(df_cust['is_repeat'].mean() * 100):.1f}%")
col3.metric("Avg CLV", f"₹{df_cust['clv'].mean():,.2f}")
col4.metric("Top Spender", f"₹{df_cust['total_spent'].max():,.2f}")
col5.metric("At-Risk Customers", f"{len(df_cust[df_cust['segment'] == 'At Risk / Churning']):,}")

st.markdown("---")

# Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Customer List & Search", 
    "🏆 Top Customers & Repeat Rate", 
    "📈 Growth & CLV Analysis", 
    "🎯 Customer Segmentation"
])

with tab1:
    st.subheader("Customer List & Profile Lookup")
    search_term = st.text_input("🔍 Search by Customer Name or ID", "")
    
    # Safe string search handling numeric customer_id & null values
    filtered_df = df_cust[
        df_cust["customer_name"].str.contains(search_term, case=False, na=False) |
        df_cust["customer_id"].str.contains(search_term, case=False, na=False)
    ]
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

with tab2:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Top 10 High-Value Customers")
        top_10 = df_cust.sort_values(by="total_spent", ascending=False).head(10)
        fig_top = px.bar(top_10, x="total_spent", y="customer_name", orientation="h",
                         labels={"total_spent": "Total Spent (₹)", "customer_name": "Customer"},
                         color="total_spent", color_continuous_scale="Viridis")
        fig_top.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_top, use_container_width=True)
    
    with c2:
        st.subheader("Repeat vs Single Order Breakdown")
        repeat_counts = df_cust["is_repeat"].map({True: "Repeat Customer", False: "One-Time Buyer"}).value_counts()
        fig_pie = px.pie(values=repeat_counts.values, names=repeat_counts.index, 
                         color_discrete_sequence=px.colors.qualitative.Set2, hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

with tab3:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Customer Acquisition Growth")
        growth_df = df_cust.groupby(df_cust["join_date"].dt.to_period("M")).size().reset_index(name="new_customers")
        growth_df["join_date"] = growth_df["join_date"].astype(str)
        fig_growth = px.line(growth_df, x="join_date", y="new_customers", markers=True, title="Monthly New Customer Growth")
        st.plotly_chart(fig_growth, use_container_width=True)
        
    with c2:
        st.subheader("Customer Lifetime Value (CLV) Distribution")
        fig_clv = px.histogram(df_cust, x="clv", nbins=20, color_discrete_sequence=["#2ca02c"],
                              title="Distribution of Estimated CLV (₹)")
        st.plotly_chart(fig_clv, use_container_width=True)

with tab4:
    st.subheader("RFM & Behavioral Customer Segmentation")
    fig_seg = px.pie(df_cust, names="segment", title="Customer Base Segmentation", hole=0.4)
    st.plotly_chart(fig_seg, use_container_width=True)
    st.dataframe(df_cust[["customer_id", "customer_name", "total_orders", "total_spent", "clv", "segment"]], use_container_width=True)


'''


Is Page Me Kya-Kya Ban Gaya Hai?
Customer List: Search feature ke saath poori Directory Table (tab_list).

Top Customers: Highest spend karne waale top 10 VIP customers (tab_top).

Customer Growth: Monthly new user acquisition ka Line Chart.

Repeat Customers: Repeat vs One-Time buyers ka Bar Chart.

Customer Lifetime Value (CLV): Total LTV calculation aur Orders vs CLV Scatter plot.

Customer Segmentation: RFM Segments (Champions, At Risk, Loyal) ka Donut Chart.


'''