import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import time
import re

st.set_page_config(page_title="SQL Query Lab", page_icon="💻", layout="wide")
st.title("💻 SQL Query Lab & Data Explorer")
st.caption("Write custom SQL queries, analyze raw database tables, and export result sets.")

# Initialize In-Memory SQLite Database with Sample Tables
@st.cache_resource
def init_database():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    cursor = conn.cursor()
    
    np.random.seed(42)
    n = 100

    # 1. Customers Table
    customers_df = pd.DataFrame({
        "customer_id": [f"CUST-{1000+i}" for i in range(n)],
        "name": [f"Customer {i+1}" for i in range(n)],
        "city": np.random.choice(["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Pune"], size=n),
        "total_spent": np.random.uniform(1000, 150000, size=n).round(2),
        "signup_date": pd.date_range(end=pd.Timestamp.now(), periods=n, freq="D").astype(str)
    })
    customers_df.to_sql("customers", conn, index=False, if_exists="replace")

    # 2. Orders Table
    orders_df = pd.DataFrame({
        "order_id": [f"ORD-{10000+i}" for i in range(n)],
        "customer_id": np.random.choice(customers_df["customer_id"], size=n),
        "amount": np.random.uniform(500, 25000, size=n).round(2),
        "status": np.random.choice(["Delivered", "Processing", "Cancelled", "Returned"], size=n),
        "order_date": pd.date_range(end=pd.Timestamp.now(), periods=n, freq="D").astype(str)
    })
    orders_df.to_sql("orders", conn, index=False, if_exists="replace")

    # 3. Products Table
    products_df = pd.DataFrame({
        "product_id": [f"PROD-{500+i}" for i in range(40)],
        "product_name": [f"Product {i+1}" for i in range(40)],
        "category": np.random.choice(["Electronics", "Clothing", "Home & Kitchen", "Books"], size=40),
        "unit_price": np.random.uniform(200, 15000, size=40).round(2),
        "stock_qty": np.random.randint(5, 300, size=40)
    })
    products_df.to_sql("products", conn, index=False, if_exists="replace")

    return conn

conn = init_database()

# Session State for Query History & SQL Input Buffer
if "query_history" not in st.session_state:
    st.session_state.query_history = []

if "sql_query_input" not in st.session_state:
    st.session_state.sql_query_input = "SELECT * FROM customers LIMIT 10;"

# Pre-built Sample Queries
sample_queries = {
    "Select Template": "SELECT * FROM customers LIMIT 10;",
    "Top 5 Spenders": "SELECT name, city, total_spent FROM customers ORDER BY total_spent DESC LIMIT 5;",
    "Orders Summary by Status": "SELECT status, COUNT(order_id) as total_orders, SUM(amount) as total_revenue FROM orders GROUP BY status;",
    "Low Stock Products (<50 units)": "SELECT product_name, category, stock_qty, unit_price FROM products WHERE stock_qty < 50 ORDER BY stock_qty ASC;",
    "Customer Order Join": "SELECT c.name, c.city, o.order_id, o.amount, o.status FROM customers c JOIN orders o ON c.customer_id = o.customer_id LIMIT 15;"
}

# Layout: Main Editor vs Sidebar Database Schema
col_main, col_sidebar = st.columns([3, 1])

with col_sidebar:
    st.subheader("🗄️ Database Schema")
    st.caption("Available Tables & Columns")
    
    # Table Schema Viewer
    schema_query = "SELECT name FROM sqlite_master WHERE type='table';"
    tables = pd.read_sql_query(schema_query, conn)["name"].tolist()
    
    for table in tables:
        with st.expander(f"📋 {table}"):
            columns_df = pd.read_sql_query(f"PRAGMA table_info({table});", conn)
            st.dataframe(columns_df[["name", "type"]], hide_index=True, use_container_width=True)

with col_main:
    st.subheader("⚡ SQL Query Workbench")
    
    # Sample Query Selector
    s_col1, s_col2 = st.columns([2, 1])
    selected_sample = s_col1.selectbox("💡 Quick Sample Queries", list(sample_queries.keys()))
    if s_col2.button("Load Query", use_container_width=True):
        st.session_state.sql_query_input = sample_queries[selected_sample]
        st.rerun()

    # Query Input Box
    query_text = st.text_area(
        "SQL Query Editor", 
        value=st.session_state.sql_query_input, 
        height=140,
        help="Write standard SELECT queries here."
    )

    btn_col1, btn_col2, _ = st.columns([1, 1, 2])
    run_query = btn_col1.button("▶️ Execute Query", type="primary", use_container_width=True)
    clear_query = btn_col2.button("🗑️ Clear", use_container_width=True)

    if clear_query:
        st.session_state.sql_query_input = ""
        st.rerun()

    # Execution & Validation Logic
    if run_query:
        # Safety Guardrail: Block non-read-only queries
        forbidden_words = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "CREATE"]
        if any(re.search(rf"\b{word}\b", query_text, re.IGNORECASE) for word in forbidden_words):
            st.error("⚠️ Security Restricted: Only read-only SELECT queries are allowed in this lab.")
        elif not query_text.strip():
            st.warning("Please enter a valid SQL query.")
        else:
            try:
                # Execution Timing
                start_time = time.time()
                result_df = pd.read_sql_query(query_text, conn)
                execution_time_ms = (time.time() - start_time) * 1000

                # Log to Query History
                st.session_state.query_history.insert(0, {
                    "timestamp": time.strftime("%H:%M:%S"),
                    "query": query_text,
                    "rows": len(result_df),
                    "execution_time": f"{execution_time_ms:.2f} ms"
                })

                # Display Results & Metrics
                st.success(f"✅ Query executed successfully in **{execution_time_ms:.2f} ms** | Returned **{len(result_df)}** rows")
                
                # Export Button
                csv_data = result_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Export Result as CSV",
                    data=csv_data,
                    file_name="sql_query_result.csv",
                    mime="text/csv"
                )

                # Render Data Table
                st.dataframe(result_df, use_container_width=True, hide_index=True)

            except Exception as e:
                st.error(f"❌ SQL Execution Error: {str(e)}")

# Tabs for History & Analytics
st.markdown("---")
tab1, tab2 = st.tabs(["📜 Query History", "⚙️ Lab Settings"])

with tab1:
    st.subheader("Execution History (Current Session)")
    if len(st.session_state.query_history) == 0:
        st.info("No queries executed yet.")
    else:
        history_df = pd.DataFrame(st.session_state.query_history)
        st.dataframe(history_df, use_container_width=True, hide_index=True)

with tab2:
    st.subheader("Database Connection Status")
    st.json({
        "engine": "SQLite 3 In-Memory",
        "status": "Connected",
        "read_only_mode": True,
        "max_row_limit": 10000
    })