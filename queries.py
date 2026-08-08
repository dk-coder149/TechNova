# import pandas as pd
# import streamlit as st
# from db_connection import get_db_engine


# @st.cache_data(ttl=3600, show_spinner=False)
# def load_dashboard_summary():
#     """Fetch pre-computed daily sales summary data."""
#     engine = get_db_engine()  # Function ke andar engine call karein
#     query = "SELECT * FROM daily_sales_summary;"
#     return pd.read_sql(query, engine)


# @st.cache_data(ttl=3600, show_spinner=False)
# def load_rfm_data():
#     """Fetch Customer Spending and Order History."""
#     engine = get_db_engine()
#     query = """
#     SELECT 
#         c.customer_id,
#         CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
#         COUNT(DISTINCT o.order_id) AS total_orders,
#         SUM(oi.selling_price) AS total_spent
#     FROM customers c
#     JOIN orders o ON c.customer_id = o.customer_id
#     JOIN order_items oi ON o.order_id = oi.order_id
#     GROUP BY c.customer_id, customer_name
#     LIMIT 1000;
#     """
#     return pd.read_sql(query, engine)


# @st.cache_data(ttl=3600, show_spinner=False)
# def load_low_inventory():
#     """Fetch Low Stock Items for Inventory Alert."""
#     engine = get_db_engine()
#     query = """
#     SELECT 
#         p.product_name,
#         c.category_name,
#         i.stock_quantity,
#         i.reorder_level
#     FROM inventory i
#     JOIN products p ON i.product_id = p.product_id
#     JOIN categories c ON p.category_id = c.category_id
#     WHERE i.stock_quantity <= i.reorder_level
#     ORDER BY i.stock_quantity ASC
#     LIMIT 20;
#     """
#     return pd.read_sql(query, engine)





import pandas as pd
import streamlit as st
from db_connection import get_db_engine


# -----------------------------------------------------------------
# 1. MAIN DASHBOARD FUNCTIONS
# -----------------------------------------------------------------
@st.cache_data(ttl=3600, show_spinner=False)
def load_dashboard_summary():
    """Fetch pre-computed daily sales summary data."""
    engine = get_db_engine()
    query = "SELECT * FROM daily_sales_summary;"
    return pd.read_sql(query, engine)


@st.cache_data(ttl=3600, show_spinner=False)
def load_low_inventory():
    """Fetch Low Stock Items for Inventory Alert."""
    engine = get_db_engine()
    query = """
    SELECT 
        p.product_name,
        c.category_name,
        i.stock_quantity,
        i.reorder_level
    FROM inventory i
    JOIN products p ON i.product_id = p.product_id
    JOIN categories c ON p.category_id = c.category_id
    WHERE i.stock_quantity <= i.reorder_level
    ORDER BY i.stock_quantity ASC
    LIMIT 20;
    """
    return pd.read_sql(query, engine)


# -----------------------------------------------------------------
# 2. CUSTOMER ANALYTICS FUNCTIONS
# -----------------------------------------------------------------
@st.cache_data(ttl=3600, show_spinner=False)
def load_rfm_data():
    """Fetch Customer Spending and Order History."""
    engine = get_db_engine()
    query = """
    SELECT 
        c.customer_id,
        CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
        COUNT(DISTINCT o.order_id) AS total_orders,
        SUM(oi.quantity * oi.selling_price) AS total_spent
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY c.customer_id, customer_name
    LIMIT 1000;
    """
    return pd.read_sql(query, engine)


# -----------------------------------------------------------------
# 3. PRODUCTS ANALYTICS FUNCTIONS
# -----------------------------------------------------------------
@st.cache_data(ttl=3600, show_spinner=False)
def load_product_analytics():
    """Fetch Product performance, revenue, profit, and stock data."""
    engine = get_db_engine()
    query = """
    SELECT 
        p.product_id,
        p.product_name,
        c.category_name AS category,
        p.cost_price,
        p.selling_price,
        COALESCE(SUM(oi.quantity), 0) AS units_sold,
        COALESCE(SUM(oi.quantity * oi.selling_price), 0) AS revenue,
        COALESCE(SUM(oi.quantity * (oi.selling_price - p.cost_price)), 0) AS profit,
        ROUND(((p.selling_price - p.cost_price) / p.selling_price) * 100, 2) AS margin_percentage,
        COALESCE(i.stock_quantity, 0) AS stock_quantity
    FROM products p
    LEFT JOIN categories c ON p.category_id = c.category_id
    LEFT JOIN order_items oi ON p.product_id = oi.product_id
    LEFT JOIN inventory i ON p.product_id = i.product_id
    GROUP BY p.product_id, p.product_name, c.category_name, p.cost_price, p.selling_price, i.stock_quantity;
    """
    return pd.read_sql(query, engine)


# -----------------------------------------------------------------
# 4. ORDERS ANALYTICS FUNCTIONS
# -----------------------------------------------------------------
@st.cache_data(ttl=3600, show_spinner=False)
def load_orders_analytics():
    """Fetch Order status, payment methods, channel, and delivery details."""
    engine = get_db_engine()
    query = """
    SELECT 
        o.order_id,
        o.order_date,
        o.status,
        o.payment_method,
        o.sales_channel,
        SUM(oi.quantity * oi.selling_price) AS order_amount,
        DATEDIFF(o.delivery_date, o.order_date) AS delivery_days
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY o.order_id, o.order_date, o.status, o.payment_method, o.sales_channel, delivery_days;
    """
    return pd.read_sql(query, engine)


# -----------------------------------------------------------------
# 5. SALES ANALYTICS FUNCTIONS
# -----------------------------------------------------------------
@st.cache_data(ttl=3600, show_spinner=False)
def load_sales_analytics():
    """Fetch Monthly sales trend, discounts, returns, and targets."""
    engine = get_db_engine()
    query = """
    SELECT 
        DATE_FORMAT(s.sales_month, '%b %Y') AS month,
        s.gross_sales,
        s.discounts,
        s.returns,
        (s.gross_sales - s.discounts - s.returns) AS net_sales,
        s.target_amount AS target
    FROM monthly_sales_summary s
    ORDER BY s.sales_month ASC;
    """
    return pd.read_sql(query, engine)


# -----------------------------------------------------------------
# 6. EMPLOYEES ANALYTICS FUNCTIONS
# -----------------------------------------------------------------
@st.cache_data(ttl=3600, show_spinner=False)
def load_employee_analytics():
    """Fetch Employee sales achievements, targets, and region metrics."""
    engine = get_db_engine()
    query = """
    SELECT 
        e.employee_id,
        CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
        e.region,
        e.sales_target,
        COALESCE(SUM(o.order_amount), 0) AS sales_achieved,
        COUNT(o.order_id) AS deals_closed,
        ROUND((COALESCE(SUM(o.order_amount), 0) / e.sales_target) * 100, 2) AS achievement_rate
    FROM employees e
    LEFT JOIN orders o ON e.employee_id = o.sales_rep_id
    GROUP BY e.employee_id, employee_name, e.region, e.sales_target;
    """
    return pd.read_sql(query, engine)


# -----------------------------------------------------------------
# 7. INVENTORY ANALYTICS FUNCTIONS
# -----------------------------------------------------------------
@st.cache_data(ttl=3600, show_spinner=False)
def load_inventory_analytics():
    """Fetch Full Inventory list, valuation, and reorder warnings."""
    engine = get_db_engine()
    query = """
    SELECT 
        i.sku_id,
        p.product_name AS item_name,
        c.category_name AS category,
        i.stock_quantity AS current_stock,
        i.reorder_level,
        p.cost_price AS unit_cost,
        (i.stock_quantity * p.cost_price) AS stock_value,
        CASE 
            WHEN i.stock_quantity <= i.reorder_level THEN 'Reorder Needed'
            ELSE 'Sufficient'
        END AS reorder_status
    FROM inventory i
    JOIN products p ON i.product_id = p.product_id
    JOIN categories c ON p.category_id = c.category_id;
    """
    return pd.read_sql(query, engine)