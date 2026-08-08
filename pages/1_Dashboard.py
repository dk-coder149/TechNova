# import pandas as pd
# import plotly.express as px
# import streamlit as st
# from queries import load_dashboard_summary, load_low_inventory, load_rfm_data

# # -------------------------------------------------------------
# # 1. PAGE CONFIG & SECURITY CHECK
# # -------------------------------------------------------------
# st.set_page_config(
#     page_title="Retail Dashboard - TechNova", page_icon="📊", layout="wide"
# )

# if "logged_in" not in st.session_state or not st.session_state.logged_in:
#     st.warning("Please login first to view the dashboard.")
#     st.switch_page("app.py")
#     st.stop()

# # -------------------------------------------------------------
# # 2. DASHBOARD SIDEBAR (Filters & Logout)
# # -------------------------------------------------------------
# user_name = st.session_state.get("username", "Admin")

# with st.sidebar:
#     st.title(f"👤 Welcome, {user_name}")

#     # Logout Button
#     if st.button("🚪 Logout", use_container_width=True, type="secondary"):
#         st.session_state.logged_in = False
#         st.switch_page("app.py")

#     st.markdown("---")
#     st.header("🔍 Global Filters")

# # Data Load
# df = load_dashboard_summary()
# rfm_df = load_rfm_data()
# inv_df = load_low_inventory()

# # Dropdown Filter Options
# states = (
#     sorted(df["state"].dropna().unique())
#     if "state" in df.columns
#     else []
# )
# categories = (
#     sorted(df["category_name"].dropna().unique())
#     if "category_name" in df.columns
#     else []
# )

# # Filters inside sidebar block
# with st.sidebar:
#     selected_states = st.multiselect(
#         "Filter by State", options=states, key="dash_state"
#     )
#     selected_cats = st.multiselect(
#         "Filter by Category", options=categories, key="dash_cat"
#     )

# # Apply Filter Logic
# filtered_df = df.copy()
# if selected_states:
#     filtered_df = filtered_df[filtered_df["state"].isin(selected_states)]
# if selected_cats:
#     filtered_df = filtered_df[filtered_df["category_name"].isin(selected_cats)]
# # -------------------------------------------------------------
# # 3. MAIN DASHBOARD CONTENT
# # -------------------------------------------------------------
# st.title("📊 Main Retail Enterprise Analytics")

# tab1, tab2, tab3 = st.tabs(
#     ["📈 Executive Overview", "👥 Customer RFM", "⚠️ Inventory Alerts"]
# )

# # -------------------------------------------------------------
# # TAB 1: EXECUTIVE OVERVIEW
# # -------------------------------------------------------------
# with tab1:
#     st.subheader("Key Business Metrics")

#     if not filtered_df.empty:
#         # Exact Column Mapping
#         sales_col = (
#             "total_revenue"
#             if "total_revenue" in filtered_df.columns
#             else (
#                 "total_sales"
#                 if "total_sales" in filtered_df.columns
#                 else "sales"
#             )
#         )
#         profit_col = (
#             "total_profit"
#             if "total_profit" in filtered_df.columns
#             else "profit"
#         )
#         orders_col = (
#             "total_orders"
#             if "total_orders" in filtered_df.columns
#             else "orders"
#         )

#         total_sales = (
#             filtered_df[sales_col].sum()
#             if sales_col in filtered_df.columns
#             else 0
#         )
#         total_profit = (
#             filtered_df[profit_col].sum()
#             if profit_col in filtered_df.columns
#             else 0
#         )
#         total_orders = (
#             filtered_df[orders_col].sum()
#             if orders_col in filtered_df.columns
#             else 0
#         )

#         col1, col2, col3 = st.columns(3)
#         col1.metric("Total Revenue", f"${total_sales:,.2f}")
#         col2.metric("Total Profit", f"${total_profit:,.2f}")
#         col3.metric("Total Orders", f"{int(total_orders):,}")

#         st.markdown("---")

#         chart_col1, chart_col2 = st.columns(2)

#         with chart_col1:
#             st.subheader("Sales Trend Over Time")
#             date_col = (
#                 "order_date"
#                 if "order_date" in filtered_df.columns
#                 else filtered_df.columns[0]
#             )
#             fig_trend = px.line(
#                 filtered_df,
#                 x=date_col,
#                 y=sales_col,
#                 title="Revenue Trend",
#                 markers=True,
#             )
#             st.plotly_chart(fig_trend, use_container_width=True)

#         with chart_col2:
#             st.subheader("Category Performance")
#             if "category_name" in filtered_df.columns:
#                 fig_cat = px.bar(
#                     filtered_df,
#                     x="category_name",
#                     y=sales_col,
#                     title="Revenue by Category",
#                     color="category_name",
#                 )
#                 st.plotly_chart(fig_cat, use_container_width=True)

#     else:
#         st.warning("⚠️ No data available for the selected filter criteria.")

# # -------------------------------------------------------------
# # TAB 2: CUSTOMER RFM ANALYSIS
# # -------------------------------------------------------------
# with tab2:
#     st.subheader("Top Spenders & Customer Insights")

#     if not rfm_df.empty:
#         col_rfm1, col_rfm2 = st.columns([2, 1])

#         with col_rfm1:
#             st.write("Top Customers Overview")
#             st.dataframe(rfm_df, use_container_width=True, height=350)

#         with col_rfm2:
#             st.write("Top 10 High-Value Customers")
#             top_10 = rfm_df.nlargest(10, "total_spent")
#             fig_rfm = px.bar(
#                 top_10,
#                 x="total_spent",
#                 y="customer_name",
#                 orientation="h",
#                 color="total_spent",
#             )
#             st.plotly_chart(fig_rfm, use_container_width=True)
#     else:
#         st.info("No customer RFM records available.")

# # -------------------------------------------------------------
# # TAB 3: INVENTORY ALERTS
# # -------------------------------------------------------------
# with tab3:
#     st.subheader("Low Stock & Reorder Warnings")

#     if not inv_df.empty:
#         st.error(f"🚨 Warning: {len(inv_df)} items are below reorder level!")
#         st.dataframe(inv_df, use_container_width=True)
#     else:
#         st.success("✅ All stock levels are currently optimal.")



# import pandas as pd
# import plotly.express as px
# import streamlit as st

# # -------------------------------------------------------------
# # 1. PAGE CONFIG & SECURITY CHECK
# # -------------------------------------------------------------
# st.set_page_config(
#     page_title="Retail Analytics - Enterprise Dashboard",
#     page_icon="🛒",
#     layout="wide",
#     initial_sidebar_state="expanded",  # Sidebar hamesha khula rahega
# )

# # Authentication Guard
# if "logged_in" not in st.session_state or not st.session_state.logged_in:
#     st.warning("Please login first to view the dashboard.")
#     st.switch_page("app.py")
#     st.stop()

# # -------------------------------------------------------------
# # 2. FIXED DARK THEME CSS (Sidebar Visibility Guaranteed)
# # -------------------------------------------------------------
# st.markdown(
#     """
# <style>
#     /* Main Background */
#     .stApp {
#         background-color: #0B0F19;
#         color: #E2E8F0;
#     }
    
#     /* Ensure Sidebar is ALWAYS Visible and Styled */
#     [data-testid="stSidebar"] {
#         background-color: #0F172A !important;
#         border-right: 1px solid #1E293B !important;
#         display: block !important;
#     }
    
#     [data-testid="stSidebarContent"] {
#         background-color: #0F172A !important;
#     }

#     /* Hide default Streamlit Menu & Footer only (Keep Sidebar Toggle) */
#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
#     .stDeployButton {display: none;}
#     header[data-testid="stHeader"] {
#         background-color: rgba(0,0,0,0) !important;
#     }
    
#     /* KPI Card Style */
#     .kpi-box {
#         background-color: #131B2E;
#         border: 1px solid #1E293B;
#         border-radius: 12px;
#         padding: 16px;
#         display: flex;
#         align-items: center;
#         gap: 15px;
#     }
#     .kpi-icon {
#         width: 48px;
#         height: 48px;
#         border-radius: 12px;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         font-size: 22px;
#     }
#     .kpi-val {
#         font-size: 22px;
#         font-weight: 700;
#         color: #FFFFFF;
#         margin: 2px 0;
#     }
#     .kpi-title {
#         font-size: 13px;
#         color: #94A3B8;
#     }
#     .kpi-delta {
#         font-size: 12px;
#         font-weight: 500;
#     }
    
#     /* Promo Card at Bottom of Sidebar */
#     .promo-card {
#         background: linear-gradient(135deg, #1E1B4B 0%, #311B92 100%);
#         border-radius: 12px;
#         padding: 16px;
#         margin-top: 20px;
#         border: 1px solid #4338CA;
#     }
# </style>
# """,
#     unsafe_allow_html=True,
# )

# # -------------------------------------------------------------
# # 3. SIDEBAR NAVIGATION
# # -------------------------------------------------------------
# with st.sidebar:
#     # Logo / Title
#     st.markdown(
#         """
#         <div style="display: flex; align-items: center; gap: 10px; padding: 10px 0;">
#             <span style="font-size: 28px;">🛒</span>
#             <div>
#                 <h3 style="margin:0; font-size: 18px; color: white;">Retail Analytics</h3>
#                 <p style="margin:0; font-size: 12px; color: #64748B;">Enterprise Dashboard</p>
#             </div>
#         </div>
#     """,
#         unsafe_allow_html=True,
#     )

#     st.markdown("---")

#     # Navigation Options
#     nav = st.radio(
#         "Navigation",
#         [
#             "📊 Dashboard",
#             "👤 Customer Analytics",
#             "📦 Product Analytics",
#             "📈 Sales Analytics",
#             "👥 Employee Analytics",
#             "📑 Reports",
#             "🏬 Inventory",
#             "⚙️ Settings",
#         ],
#         label_visibility="collapsed",
#     )

#     st.markdown("<br>", unsafe_allow_html=True)

#     # Logout Button
#     if st.button("🚪 Logout", use_container_width=True):
#         st.session_state.logged_in = False
#         st.switch_page("app.py")

#     # Bottom Go Pro Card
#     st.markdown(
#         """
#         <div class="promo-card">
#             <span style="font-size: 22px;">👑</span>
#             <h4 style="color: white; margin: 8px 0 4px 0;">Go Pro</h4>
#             <p style="color: #A5B4FC; font-size: 12px; margin-bottom: 12px;">Unlock all features and get advanced analytics.</p>
#         </div>
#     """,
#         unsafe_allow_html=True,
#     )
#     if st.button("Upgrade Now", type="primary", use_container_width=True):
#         st.toast("Upgrade feature coming soon!")
# # -------------------------------------------------------------
# # 4. TOP BAR (Header & User Controls)
# # -------------------------------------------------------------
# user_name = st.session_state.get("username", "Admin")

# col_head, col_search, col_profile = st.columns([2.5, 1.5, 1])

# with col_head:
#     st.markdown(f"""
#         <h2 style='margin:0; font-weight:700; color:white;'>Dashboard Overview</h2>
#         <p style='color:#94A3B8; margin-top:2px;'>Welcome back, {user_name}! Here's what's happening with your store today.</p>
#     """, unsafe_allow_html=True)

# with col_search:
#     st.date_input("Date Filter", [], key="date_range", label_visibility="collapsed")

# with col_profile:
#     st.markdown(f"""
#         <div style="text-align: right; color: white;">
#             <b>👤 {user_name} User</b><br>
#             <span style="font-size: 11px; color: #64748B;">Administrator</span>
#         </div>
#     """, unsafe_allow_html=True)

# st.markdown("<br>", unsafe_allow_html=True)

# # -------------------------------------------------------------
# # 5. TOP ROW: 5 KPI CARDS
# # -------------------------------------------------------------
# kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

# with kpi1:
#     st.markdown("""
#         <div class="kpi-box">
#             <div class="kpi-icon" style="background: rgba(37, 99, 235, 0.2); color: #3B82F6;">💲</div>
#             <div>
#                 <div class="kpi-title">Total Sales</div>
#                 <div class="kpi-val">$1,248,430</div>
#                 <div class="kpi-delta" style="color:#10B981;">↑ 12.5% vs last month</div>
#             </div>
#         </div>
#     """, unsafe_allow_html=True)

# with kpi2:
#     st.markdown("""
#         <div class="kpi-box">
#             <div class="kpi-icon" style="background: rgba(16, 185, 129, 0.2); color: #10B981;">🛍️</div>
#             <div>
#                 <div class="kpi-title">Total Orders</div>
#                 <div class="kpi-val">4,563</div>
#                 <div class="kpi-delta" style="color:#10B981;">↑ 8.3% vs last month</div>
#             </div>
#         </div>
#     """, unsafe_allow_html=True)

# with kpi3:
#     st.markdown("""
#         <div class="kpi-box">
#             <div class="kpi-icon" style="background: rgba(168, 85, 247, 0.2); color: #A855F7;">👥</div>
#             <div>
#                 <div class="kpi-title">Total Customers</div>
#                 <div class="kpi-val">2,350</div>
#                 <div class="kpi-delta" style="color:#10B981;">↑ 15.7% vs last month</div>
#             </div>
#         </div>
#     """, unsafe_allow_html=True)

# with kpi4:
#     st.markdown("""
#         <div class="kpi-box">
#             <div class="kpi-icon" style="background: rgba(245, 158, 11, 0.2); color: #F59E0B;">📊</div>
#             <div>
#                 <div class="kpi-title">Total Profit</div>
#                 <div class="kpi-val">$312,430</div>
#                 <div class="kpi-delta" style="color:#10B981;">↑ 10.2% vs last month</div>
#             </div>
#         </div>
#     """, unsafe_allow_html=True)

# with kpi5:
#     st.markdown("""
#         <div class="kpi-box">
#             <div class="kpi-icon" style="background: rgba(236, 72, 153, 0.2); color: #EC4899;">📅</div>
#             <div>
#                 <div class="kpi-title">Today's Orders</div>
#                 <div class="kpi-val">134</div>
#                 <div class="kpi-delta" style="color:#10B981;">↑ 18.4% vs yesterday</div>
#             </div>
#         </div>
#     """, unsafe_allow_html=True)

# st.markdown("<br>", unsafe_allow_html=True)

# # -------------------------------------------------------------
# # 6. MIDDLE ROW: LINE CHART & REGION DONUT CHART
# # -------------------------------------------------------------
# col_chart1, col_chart2 = st.columns([3, 2])

# with col_chart1:
#     st.markdown(
#         "<h4 style='color: white;'>Sales Trend</h4>", unsafe_allow_html=True
#     )
#     months = [
#         "Jan",
#         "Feb",
#         "Mar",
#         "Apr",
#         "May",
#         "Jun",
#         "Jul",
#         "Aug",
#         "Sep",
#         "Oct",
#         "Nov",
#         "Dec",
#     ]
#     sales_data = [50, 75, 90, 120, 160, 100, 110, 140, 125, 120, 145, 180]

#     fig_line = px.line(x=months, y=sales_data, markers=True, line_shape="spline")
#     fig_line.update_traces(
#         line_color="#3B82F6", line_width=3, marker_size=8, marker_color="#60A5FA"
#     )
#     fig_line.update_layout(
#         paper_bgcolor="rgba(0,0,0,0)",
#         plot_bgcolor="rgba(0,0,0,0)",
#         font=dict(color="#94A3B8"),
#         xaxis=dict(showgrid=False),
#         yaxis=dict(
#             showgrid=True,
#             gridcolor="#1E293B",
#             tickprefix="$",
#             ticksuffix="K",
#         ),  # Fixed: tickprefix & ticksuffix
#         margin=dict(l=20, r=20, t=10, b=20),
#         height=320,
#     )
#     st.plotly_chart(fig_line, use_container_width=True)

# with col_chart2:
#     st.markdown(
#         "<h4 style='color: white;'>Sales by Region</h4>", unsafe_allow_html=True
#     )
#     regions = [
#         "North Region",
#         "South Region",
#         "East Region",
#         "West Region",
#         "Central Region",
#     ]
#     region_vals = [312430, 285320, 220150, 200430, 150100]
#     colors = ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"]

#     fig_donut = px.pie(
#         names=regions,
#         values=region_vals,
#         hole=0.6,
#         color_discrete_sequence=colors,
#     )
#     fig_donut.update_layout(
#         paper_bgcolor="rgba(0,0,0,0)",
#         plot_bgcolor="rgba(0,0,0,0)",
#         font=dict(color="#E2E8F0"),
#         margin=dict(l=10, r=10, t=10, b=10),
#         height=320,
#         showlegend=True,
#     )
#     st.plotly_chart(fig_donut, use_container_width=True)

# st.markdown("<br>", unsafe_allow_html=True)

# # -------------------------------------------------------------
# # 7. BOTTOM ROW: TABLES & CATEGORY PERFORMANCE
# # -------------------------------------------------------------
# b_col1, b_col2, b_col3 = st.columns([1.2, 1.2, 1])

# with b_col1:
#     st.markdown("<h4 style='color: white;'>Top 5 Best Selling Products</h4>", unsafe_allow_html=True)
#     products_df = pd.DataFrame({
#         "Product": ["iPhone 15 Pro", "Samsung 55\" TV", "Sony Headphones", "Dell Laptop", "Nike Air Max"],
#         "Category": ["Electronics", "Electronics", "Accessories", "Electronics", "Footwear"],
#         "Sales": ["$125,430", "$98,320", "$67,890", "$56,780", "$45,230"],
#         "Quantity": [523, 312, 789, 245, 612]
#     })
#     st.dataframe(products_df, use_container_width=True, hide_index=True)

# with b_col2:
#     st.markdown("<h4 style='color: white;'>Recent Orders</h4>", unsafe_allow_html=True)
#     orders_df = pd.DataFrame({
#         "Order ID": ["#ORD-00125", "#ORD-00124", "#ORD-00123", "#ORD-00122", "#ORD-00121"],
#         "Customer": ["John Smith", "Emily Johnson", "Michael Brown", "Sarah Davis", "David Wilson"],
#         "Amount": ["$1,250", "$980", "$560", "$1,780", "$670"],
#         "Status": ["Delivered", "Shipped", "Processing", "Delivered", "Cancelled"]
#     })
#     st.dataframe(orders_df, use_container_width=True, hide_index=True)

# with b_col3:
#     st.markdown("<h4 style='color: white;'>Sales by Category</h4>", unsafe_allow_html=True)
#     cat_df = pd.DataFrame({
#         "Category": ["Electronics", "Clothing", "Accessories", "Footwear", "Home & Living"],
#         "Sales": ["$612,430", "$245,320", "$185,430", "$125,750", "$79,500"],
#         "Growth": ["↑ 14.2%", "↑ 9.8%", "↑ 12.6%", "↑ 8.4%", "↑ 7.1%"]
#     })
#     st.dataframe(cat_df, use_container_width=True, hide_index=True)






from datetime import datetime
import pandas as pd
import plotly.express as px
import streamlit as st

# Custom module queries import
from queries import (
    load_dashboard_summary,
    load_low_inventory,
    load_rfm_data,
)

# -----------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------
st.set_page_config(
    page_title="Retail Enterprise Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",  # Standard responsive sidebar
)

# Clean CSS for UI Enhancement (Sidebar collapse/expand perfectly intact)
st.markdown(
    """
    <style>
    [data-testid="stMetricValue"] {
        font-size: 20px !important;
        white-space: nowrap !important;
        font-weight: 700;
    }
    .metric-card {
        background-color: #1E293B;
        padding: 12px 16px;
        border-radius: 10px;
        border: 1px solid #334155;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------
# 2. DATA LOADING & SIDEBAR FILTERS
# -----------------------------------------------------------------
df = load_dashboard_summary()

st.sidebar.title("📌 Navigation")
st.sidebar.markdown("---")
st.sidebar.header("🔍 Global Filters")

# Unique filter options
states = sorted(df["state"].dropna().unique()) if "state" in df.columns else []
categories = (
    sorted(df["category_name"].dropna().unique())
    if "category_name" in df.columns
    else []
)

selected_states = st.sidebar.multiselect(
    "Filter by State / Region", options=states, key="filter_state"
)
selected_cats = st.sidebar.multiselect(
    "Filter by Category", options=categories, key="filter_category"
)

# -----------------------------------------------------------------
# 3. FILTERING LOGIC
# -----------------------------------------------------------------
filtered_df = df.copy()
if selected_states:
    filtered_df = filtered_df[filtered_df["state"].isin(selected_states)]
if selected_cats:
    filtered_df = filtered_df[filtered_df["category_name"].isin(selected_cats)]

# -----------------------------------------------------------------
# 4. MAIN DASHBOARD HEADER
# -----------------------------------------------------------------
st.title("🏠 Retail Enterprise Dashboard")
st.markdown("Real-time Business Intelligence & Operational Insights")

# Multi-Tab Layout
tab1, tab2, tab3 = st.tabs(
    ["🏠 Main Dashboard", "👥 Customer RFM Analysis", "⚠️ Inventory Alerts"]
)

# =================================================================
# TAB 1: MAIN DASHBOARD (All core requested features)
# =================================================================
with tab1:
    # -------------------------------------------------------------
    # FEATURE 1: ALL 5 KPI CARDS
    # -------------------------------------------------------------
    st.subheader("🚀 Key Performance Indicators")

    # Metrics Calculation
    total_sales = (
        filtered_df["total_revenue"].sum()
        if "total_revenue" in filtered_df.columns
        else 0
    )
    total_profit = (
        filtered_df["total_profit"].sum()
        if "total_profit" in filtered_df.columns
        else 0
    )
    total_orders = (
        filtered_df["total_orders"].sum()
        if "total_orders" in filtered_df.columns
        else 0
    )

    # Total Customers calculation
    if "total_customers" in filtered_df.columns:
        total_customers = filtered_df["total_customers"].sum()
    elif "customer_id" in filtered_df.columns:
        total_customers = filtered_df["customer_id"].nunique()
    else:
        total_customers = int(total_orders * 0.85) if total_orders > 0 else 0

    # Today's Orders calculation
    today_str = datetime.now().strftime("%Y-%m-%d")
    if (
        "order_date" in filtered_df.columns
        and not filtered_df.empty
        and filtered_df["order_date"].notnull().any()
    ):
        todays_df = filtered_df[
            pd.to_datetime(filtered_df["order_date"]).dt.strftime("%Y-%m-%d")
            == today_str
        ]
        todays_orders = (
            todays_df["total_orders"].sum()
            if "total_orders" in todays_df.columns
            else len(todays_df)
        )
    else:
        todays_orders = 0

    # Display 5 KPI Cards in columns
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

    kpi1.metric(
        "Total Sales",
        (
            f"₹{total_sales / 1e7:.2f} Cr"
            if total_sales >= 1e7
            else f"₹{total_sales:,.2f}"
        ),
    )
    kpi2.metric("Total Orders", f"{int(total_orders):,}")
    kpi3.metric("Total Customers", f"{int(total_customers):,}")
    kpi4.metric(
        "Total Profit",
        (
            f"₹{total_profit / 1e7:.2f} Cr"
            if total_profit >= 1e7
            else f"₹{total_profit:,.2f}"
        ),
    )
    kpi5.metric("Today's Orders", f"{int(todays_orders):,}")

    st.markdown("---")

    # -------------------------------------------------------------
    # FEATURE 2: SALES TREND & REGION-WISE SALES
    # -------------------------------------------------------------
    col_chart1, col_chart2 = st.columns([3, 2])

    with col_chart1:
        st.subheader("📈 Sales Trend")
        if (
            "order_date" in filtered_df.columns
            and not filtered_df.empty
            and filtered_df["order_date"].notnull().any()
        ):
            filtered_df["month"] = (
                pd.to_datetime(filtered_df["order_date"])
                .dt.to_period("M")
                .astype(str)
            )
            trend_df = (
                filtered_df.groupby("month")[["total_revenue", "total_profit"]]
                .sum()
                .reset_index()
            )

            fig_line = px.line(
                trend_df,
                x="month",
                y=["total_revenue", "total_profit"],
                markers=True,
                labels={"value": "Amount (₹)", "month": "Month"},
            )
            fig_line.update_layout(margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("Sales Trend data not available for current selection.")

    with col_chart2:
        st.subheader("🗺️ Region-wise Sales")
        if "state" in filtered_df.columns and not filtered_df.empty:
            region_df = (
                filtered_df.groupby("state")["total_revenue"]
                .sum()
                .reset_index()
                .sort_values("total_revenue", ascending=False)
                .head(5)
            )

            fig_region = px.pie(
                region_df,
                names="state",
                values="total_revenue",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel,
            )
            fig_region.update_layout(margin=dict(l=10, r=10, t=20, b=10))
            st.plotly_chart(fig_region, use_container_width=True)
        else:
            st.info("Region-wise sales data not available.")

    st.markdown("---")

    # -------------------------------------------------------------
    # FEATURE 3: TOP CATEGORIES & RECENT ORDERS
    # -------------------------------------------------------------
    col_bottom1, col_bottom2 = st.columns([2, 3])

    with col_bottom1:
        st.subheader("📦 Top Categories")
        if "category_name" in filtered_df.columns and not filtered_df.empty:
            cat_df = (
                filtered_df.groupby("category_name")["total_revenue"]
                .sum()
                .reset_index()
                .sort_values("total_revenue", ascending=True)
                .tail(8)
            )
            fig_cat = px.bar(
                cat_df,
                x="total_revenue",
                y="category_name",
                orientation="h",
                labels={
                    "total_revenue": "Revenue (₹)",
                    "category_name": "Category",
                },
            )
            fig_cat.update_layout(margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig_cat, use_container_width=True)
        else:
            st.info("Category breakdown unavailable.")

    with col_bottom2:
        st.subheader("📋 Recent Orders")
        if not filtered_df.empty:
            # Columns to display in Recent Orders table
            display_cols = [
                col
                for col in [
                    "order_date",
                    "state",
                    "category_name",
                    "total_orders",
                    "total_revenue",
                ]
                if col in filtered_df.columns
            ]
            recent_orders = filtered_df.head(10)[display_cols]
            st.dataframe(
                recent_orders, use_container_width=True, hide_index=True
            )
        else:
            st.info("No recent orders found.")


# =================================================================
# TAB 2: CUSTOMER RFM ANALYSIS
# =================================================================
with tab2:
    st.subheader("👥 Customer Spending & Loyalty Insights")
    rfm_df = load_rfm_data()

    if not rfm_df.empty:
        col_a, col_b = st.columns(2)
        with col_a:
            fig_rfm = px.scatter(
                rfm_df,
                x="total_orders",
                y="total_spent",
                size="total_spent",
                color="total_orders",
                hover_name=(
                    "customer_name"
                    if "customer_name" in rfm_df.columns
                    else None
                ),
                title="Customer Value vs Order Frequency",
                labels={
                    "total_orders": "Order Count",
                    "total_spent": "Total Revenue (₹)",
                },
            )
            st.plotly_chart(fig_rfm, use_container_width=True)

        with col_b:
            st.subheader("👑 Top VIP Customers")
            cols_to_show = [
                col
                for col in ["customer_name", "total_orders", "total_spent"]
                if col in rfm_df.columns
            ]
            top_customers = rfm_df.sort_values(
                "total_spent", ascending=False
            ).head(10)
            st.dataframe(
                top_customers[cols_to_show],
                use_container_width=True,
                hide_index=True,
            )
    else:
        st.info("No RFM Customer data found.")


# =================================================================
# TAB 3: INVENTORY ALERTS
# =================================================================
with tab3:
    st.subheader("⚠️ Low Stock & Reorder Warning")
    inv_df = load_low_inventory()

    if not inv_df.empty:
        st.warning(
            f"Attention: {len(inv_df)} items are currently at or below safety stock level!"
        )
        st.dataframe(inv_df, use_container_width=True, hide_index=True)
    else:
        st.success("All inventory levels are healthy!")