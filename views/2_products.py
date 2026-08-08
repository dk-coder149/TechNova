import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


# -----------------------------------------------------------------
# 1. HELPER FUNCTION (Data Load with Fallback)
# -----------------------------------------------------------------
@st.cache_data
def get_product_data():
    try:
        from queries import load_product_analytics

        return load_product_analytics()
    except Exception:
        # Database Fallback / Mock Data (taaki app crash na ho)
        np.random.seed(101)
        n_products = 100

        categories = [
            "Electronics",
            "Clothing",
            "Home & Kitchen",
            "Books",
            "Beauty & Health",
            "Sports",
        ]
        prod_cats = np.random.choice(
            categories, size=n_products, p=[0.25, 0.2, 0.2, 0.15, 0.1, 0.1]
        )
        cost_prices = np.random.uniform(200, 15000, size=n_products).round(2)
        margins = np.random.uniform(0.12, 0.45, size=n_products)
        selling_prices = (cost_prices * (1 + margins)).round(2)
        units_sold = np.random.randint(10, 850, size=n_products)
        stock_qty = np.random.randint(0, 120, size=n_products)

        df = pd.DataFrame(
            {
                "product_id": [f"PROD-{1000+i}" for i in range(n_products)],
                "product_name": [
                    f"Item Model {chr(65 + (i%26))}{i+1}"
                    for i in range(n_products)
                ],
                "category": prod_cats,
                "cost_price": cost_prices,
                "selling_price": selling_prices,
                "units_sold": units_sold,
                "stock_quantity": stock_qty,
            }
        )

        # Derived metrics
        df["revenue"] = (df["selling_price"] * df["units_sold"]).round(2)
        df["profit"] = (
            (df["selling_price"] - df["cost_price"]) * df["units_sold"]
        ).round(2)
        df["margin_percentage"] = (
            ((df["selling_price"] - df["cost_price"]) / df["selling_price"])
            * 100
        ).round(2)

        return df


df_prod = get_product_data()

# -----------------------------------------------------------------
# 2. PAGE HEADER & SIDEBAR FILTERS
# -----------------------------------------------------------------
st.title("📦 Products Performance & Profitability Analytics")
st.markdown(
    "Deep dive into product revenues, margins, category distributions, and inventory velocity."
)

st.sidebar.header("🔍 Product Filters")

# Category Filter
all_categories = sorted(list(df_prod["category"].unique()))
selected_categories = st.sidebar.multiselect(
    "Filter by Category", options=all_categories, default=all_categories
)

# Stock Level Filter
stock_status_options = [
    "All Items",
    "In Stock (>20)",
    "Low Stock (1-20)",
    "Out of Stock (0)",
]
selected_stock_status = st.sidebar.selectbox(
    "Stock Status", stock_status_options
)

# Price Range Slider
min_price, max_price = float(df_prod["selling_price"].min()), float(
    df_prod["selling_price"].max()
)
price_range = st.sidebar.slider(
    "Selling Price Range (₹)",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price),
)

# Apply Filters
filtered_df = df_prod[
    (df_prod["category"].isin(selected_categories))
    & (df_prod["selling_price"] >= price_range[0])
    & (df_prod["selling_price"] <= price_range[1])
]

if selected_stock_status == "In Stock (>20)":
    filtered_df = filtered_df[filtered_df["stock_quantity"] > 20]
elif selected_stock_status == "Low Stock (1-20)":
    filtered_df = filtered_df[
        (filtered_df["stock_quantity"] >= 1)
        & (filtered_df["stock_quantity"] <= 20)
    ]
elif selected_stock_status == "Out of Stock (0)":
    filtered_df = filtered_df[filtered_df["stock_quantity"] == 0]

# -----------------------------------------------------------------
# 3. KPI CARDS
# -----------------------------------------------------------------
total_products = len(filtered_df)
total_revenue = filtered_df["revenue"].sum()
total_profit = filtered_df["profit"].sum()
avg_margin = (
    filtered_df["margin_percentage"].mean() if total_products > 0 else 0
)
low_stock_count = len(filtered_df[filtered_df["stock_quantity"] <= 20])

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Products", f"{total_products:,}")
k2.metric(
    "Total Revenue",
    (
        f"₹{total_revenue/1e5:.2f} L"
        if total_revenue >= 1e5
        else f"₹{total_revenue:,.2f}"
    ),
)
k3.metric(
    "Total Profit",
    (
        f"₹{total_profit/1e5:.2f} L"
        if total_profit >= 1e5
        else f"₹{total_profit:,.2f}"
    ),
)
k4.metric("Avg Profit Margin", f"{avg_margin:.1f}%")
k5.metric(
    "Stock Warnings",
    f"{low_stock_count}",
    delta="-Critical" if low_stock_count > 0 else "Optimal",
    delta_color="inverse",
)

st.markdown("---")

# -----------------------------------------------------------------
# 4. CHARTS: TOP REVENUE & CATEGORY SHARE
# -----------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top 10 Revenue Generating Products")
    if not filtered_df.empty:
        top_rev = filtered_df.sort_values(by="revenue", ascending=False).head(
            10
        )
        fig_top_rev = px.bar(
            top_rev,
            x="revenue",
            y="product_name",
            orientation="h",
            color="category",
            labels={"revenue": "Revenue (₹)", "product_name": "Product"},
            title="Top Revenue Contributors",
        )
        fig_top_rev.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig_top_rev, use_container_width=True)
    else:
        st.info("No product data available.")

with col2:
    st.subheader("📊 Category Revenue Breakdown")
    if not filtered_df.empty:
        cat_summary = (
            filtered_df.groupby("category")
            .agg({"revenue": "sum", "profit": "sum"})
            .reset_index()
        )
        fig_cat_pie = px.pie(
            cat_summary,
            names="category",
            values="revenue",
            hole=0.4,
            title="Revenue Contribution by Category",
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        st.plotly_chart(fig_cat_pie, use_container_width=True)
    else:
        st.info("No category data available.")

# -----------------------------------------------------------------
# 5. CHARTS: MARGIN VS VOLUME & SLOW-MOVING ITEMS
# -----------------------------------------------------------------
col3, col4 = st.columns(2)

with col3:
    st.subheader("💡 Profit Margin % vs Units Sold")
    if not filtered_df.empty:
        fig_margin = px.scatter(
            filtered_df,
            x="margin_percentage",
            y="units_sold",
            size="revenue",
            color="category",
            hover_name="product_name",
            labels={
                "margin_percentage": "Margin (%)",
                "units_sold": "Units Sold",
            },
            title="High Margin vs Volume Matrix",
        )
        st.plotly_chart(fig_margin, use_container_width=True)
    else:
        st.info("No scatter data available.")

with col4:
    st.subheader("🐢 Slow Moving / Low Sales Products")
    if not filtered_df.empty:
        low_units = filtered_df.sort_values(
            by="units_sold", ascending=True
        ).head(10)
        fig_low = px.bar(
            low_units,
            x="units_sold",
            y="product_name",
            orientation="h",
            color="stock_quantity",
            labels={"units_sold": "Units Sold", "product_name": "Product"},
            title="Lowest Volume Selling Items",
        )
        fig_low.update_layout(yaxis={"categoryorder": "total descending"})
        st.plotly_chart(fig_low, use_container_width=True)
    else:
        st.info("No data available.")

st.markdown("---")

# -----------------------------------------------------------------
# 6. PRODUCT DIRECTORY / SEARCH TABLE
# -----------------------------------------------------------------
st.subheader("📋 Comprehensive Product Directory")
search_term = st.text_input(
    "Search Product by Name or ID:",
    "",
    placeholder="Type product name or ID...",
)

if search_term:
    table_df = filtered_df[
        filtered_df["product_name"].str.contains(
            search_term, case=False, na=False
        )
        | filtered_df["product_id"].str.contains(
            search_term, case=False, na=False
        )
    ]
else:
    table_df = filtered_df

st.dataframe(
    table_df[
        [
            "product_id",
            "product_name",
            "category",
            "cost_price",
            "selling_price",
            "margin_percentage",
            "units_sold",
            "revenue",
            "profit",
            "stock_quantity",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)



##############################


@st.cache_data(ttl=3600)
def get_product_data():
    try:
        from queries import load_product_analytics
        df = load_product_analytics()
        if df.empty: raise ValueError
    except Exception:
        categories = ["Electronics", "Clothing", "Home & Kitchen", "Books", "Sports"]
        brands = ["Brand A", "Brand B", "Brand C", "Brand D", "Brand E"]
        np.random.seed(42)
        n = 100
        df = pd.DataFrame({
            "product_id": [f"PRD-{100+i}" for i in range(n)],
            "product_name": [f"Item {i+1}" for i in range(n)],
            "category": np.random.choice(categories, size=n),
            "brand": np.random.choice(brands, size=n),
            "units_sold": np.random.randint(5, 500, size=n),
            "selling_price": np.random.uniform(200, 20000, size=n).round(2),
            "cost_price": np.random.uniform(100, 15000, size=n).round(2),
        })
        df["revenue"] = (df["units_sold"] * df["selling_price"]).round(2)
        df["profit"] = (df["units_sold"] * (df["selling_price"] - df["cost_price"])).round(2)
    return df

df_prod = get_product_data()

# Global Product Search & Filters
c1, c2, c3 = st.columns([2, 1, 1])
search_query = c1.text_input("🔍 Product Search", "")
cat_filter = c2.selectbox("Filter Category", ["All"] + list(df_prod["category"].unique()))
brand_filter = c3.selectbox("Filter Brand", ["All"] + list(df_prod["brand"].unique()))

filtered_df = df_prod.copy()
if search_query:
    filtered_df = filtered_df[filtered_df["product_name"].str.contains(search_query, case=False)]
if cat_filter != "All":
    filtered_df = filtered_df[filtered_df["category"] == cat_filter]
if brand_filter != "All":
    filtered_df = filtered_df[filtered_df["brand"] == brand_filter]

# Metrics Row
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Products", len(filtered_df))
m2.metric("Total Units Sold", f"{filtered_df['units_sold'].sum():,}")
m3.metric("Total Revenue", f"₹{filtered_df['revenue'].sum():,.2f}")
m4.metric("Total Profit", f"₹{filtered_df['profit'].sum():,.2f}")

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📋 Product List", "🔥 Best vs Low Selling", "🏷️ Category & Brand Performance"])

with tab1:
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top 10 Best Selling Products (By Revenue)")
        best_sellers = filtered_df.sort_values(by="revenue", ascending=False).head(10)
        fig_best = px.bar(best_sellers, x="revenue", y="product_name", orientation="h", color="revenue", color_continuous_scale="Greens")
        fig_best.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_best, use_container_width=True)
        
    with col2:
        st.subheader("Bottom 10 Low Selling Products")
        low_sellers = filtered_df.sort_values(by="units_sold", ascending=True).head(10)
        fig_low = px.bar(low_sellers, x="units_sold", y="product_name", orientation="h", color="units_sold", color_continuous_scale="Reds")
        fig_low.update_layout(yaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig_low, use_container_width=True)

with tab3:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Category Performance")
        cat_perf = filtered_df.groupby("category")["revenue"].sum().reset_index()
        fig_cat = px.pie(cat_perf, values="revenue", names="category", title="Revenue Distribution by Category", hole=0.3)
        st.plotly_chart(fig_cat, use_container_width=True)
        
    with c2:
        st.subheader("Brand Performance")
        brand_perf = filtered_df.groupby("brand")["revenue"].sum().reset_index()
        fig_brand = px.bar(brand_perf, x="brand", y="revenue", color="brand", title="Revenue Share by Brand")
        st.plotly_chart(fig_brand, use_container_width=True)

