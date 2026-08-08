import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Admin Panel", page_icon="👑", layout="wide")

# ⛔ Security Guardrail: Non-admin users ko block karein
if st.session_state.get("role") != "Admin":
    st.error("⛔ Access Denied! Only Administrators are authorized to view this page.")
    st.stop()  # Iske aage ka koi bhi code render nahi hoga

st.title("👑 Admin Panel & Entity Management")
st.caption("Manage data records across Customers, Products, Employees, and User Accounts.")

# Mock Database Store in session state for dynamic interactive updates
if "admin_customers_db" not in st.session_state:
    st.session_state.admin_customers_db = pd.DataFrame([
        {"Customer ID": "CUST-1001", "Name": "Aarav Sharma", "Email": "aarav.s@gmail.com", "City": "Delhi", "Segment": "VIP"},
        {"Customer ID": "CUST-1002", "Name": "Priya Patel", "Email": "priya.p@yahoo.com", "City": "Mumbai", "Segment": "Regular"},
        {"Customer ID": "CUST-1003", "Name": "Rohan Gupta", "Email": "rohan.g@hotmail.com", "City": "Bangalore", "Segment": "Loyal"}
    ])

if "admin_products_db" not in st.session_state:
    st.session_state.admin_products_db = pd.DataFrame([
        {"SKU": "SKU-5001", "Product Name": "Wireless Headphones", "Category": "Electronics", "Unit Price (₹)": 2999.00, "Stock": 120},
        {"SKU": "SKU-5002", "Product Name": "Ergonomic Office Chair", "Category": "Home & Kitchen", "Unit Price (₹)": 8499.00, "Stock": 45},
        {"SKU": "SKU-5003", "Product Name": "Cotton Casual Shirt", "Category": "Clothing", "Unit Price (₹)": 1299.00, "Stock": 200}
    ])

if "admin_employees_db" not in st.session_state:
    st.session_state.admin_employees_db = pd.DataFrame([
        {"Emp ID": "EMP-101", "Employee Name": "Ananya Roy", "Department": "Sales", "Role": "Sales Manager", "Joining Date": "2024-03-15"},
        {"Emp ID": "EMP-102", "Employee Name": "Vikram Singh", "Department": "Logistics", "Role": "Supply Lead", "Joining Date": "2023-11-01"},
        {"Emp ID": "EMP-103", "Employee Name": "Neha Sharma", "Department": "Support", "Role": "Customer Agent", "Joining Date": "2025-01-10"}
    ])

if "admin_users_db" not in st.session_state:
    st.session_state.admin_users_db = pd.DataFrame([
        {"Username": "admin@technova.com", "Role": "Super Admin", "Status": "Active", "Last Login": "2026-08-08 12:45"},
        {"Username": "analyst@technova.com", "Role": "Data Analyst", "Status": "Active", "Last Login": "2026-08-07 18:20"},
        {"Username": "manager@technova.com", "Role": "Store Manager", "Status": "Deactivated", "Last Login": "2026-07-22 09:15"}
    ])

# Main Admin Action Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "👥 Add Customer", 
    "📦 Add Product", 
    "👨‍💼 Add Employee", 
    "🔐 Manage Users"
])

# TAB 1: Add Customer
with tab1:
    st.subheader("Add New Customer Record")
    
    with st.form("add_customer_form", clear_on_submit=True):
        c_col1, c_col2 = st.columns(2)
        cust_name = c_col1.text_input("Customer Name *", placeholder="e.g. Rahul Verma")
        cust_email = c_col2.text_input("Email Address *", placeholder="e.g. rahul@example.com")

        c_col3, c_col4 = st.columns(2)
        cust_city = c_col3.selectbox("City", ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Pune", "Kolkata", "Chennai", "Ahmedabad"])
        cust_segment = c_col4.selectbox("Customer Segment", ["Regular", "Loyal", "VIP", "New"])

        submit_cust = st.form_submit_button("➕ Register Customer", type="primary")

        if submit_cust:
            if not cust_name or not cust_email:
                st.warning("Please enter both Customer Name and Email.")
            else:
                new_id = f"CUST-{1000 + len(st.session_state.admin_customers_db) + 1}"
                new_cust = pd.DataFrame([{
                    "Customer ID": new_id,
                    "Name": cust_name,
                    "Email": cust_email,
                    "City": cust_city,
                    "Segment": cust_segment
                }])
                st.session_state.admin_customers_db = pd.concat([st.session_state.admin_customers_db, new_cust], ignore_index=True)
                st.success(f"✅ Customer '{cust_name}' registered successfully with ID: {new_id}")

    st.markdown("---")
    st.subheader("📋 Current Customer Directory")
    st.dataframe(st.session_state.admin_customers_db, use_container_width=True, hide_index=True)

# TAB 2: Add Product
with tab2:
    st.subheader("Add New Product SKU")
    
    with st.form("add_product_form", clear_on_submit=True):
        p_col1, p_col2 = st.columns(2)
        prod_name = p_col1.text_input("Product Name *", placeholder="e.g. Smart Watch Series 5")
        prod_category = p_col2.selectbox("Category", ["Electronics", "Clothing", "Home & Kitchen", "Books", "Sports"])

        p_col3, p_col4 = st.columns(2)
        prod_price = p_col3.number_input("Unit Price (₹) *", min_value=1.0, value=999.0, step=50.0)
        prod_stock = p_col4.number_input("Initial Stock Quantity *", min_value=0, value=50, step=1)

        submit_prod = st.form_submit_button("➕ Add Product to Catalog", type="primary")

        if submit_prod:
            if not prod_name:
                st.warning("Please enter the Product Name.")
            else:
                new_sku = f"SKU-{5000 + len(st.session_state.admin_products_db) + 1}"
                new_prod = pd.DataFrame([{
                    "SKU": new_sku,
                    "Product Name": prod_name,
                    "Category": prod_category,
                    "Unit Price (₹)": prod_price,
                    "Stock": prod_stock
                }])
                st.session_state.admin_products_db = pd.concat([st.session_state.admin_products_db, new_prod], ignore_index=True)
                st.success(f"✅ Product '{prod_name}' added successfully under SKU: {new_sku}")

    st.markdown("---")
    st.subheader("📋 Product Catalog Directory")
    st.dataframe(st.session_state.admin_products_db, use_container_width=True, hide_index=True)

# TAB 3: Add Employee
with tab3:
    st.subheader("Onboard New Employee")
    
    with st.form("add_employee_form", clear_on_submit=True):
        e_col1, e_col2 = st.columns(2)
        emp_name = e_col1.text_input("Employee Full Name *", placeholder="e.g. Suresh Kumar")
        emp_dept = e_col2.selectbox("Department", ["Sales", "Logistics", "Support", "Marketing", "IT & Analytics", "HR"])

        e_col3, e_col4 = st.columns(2)
        emp_role = e_col3.text_input("Designation / Role *", placeholder="e.g. Senior Analyst")
        emp_date = e_col4.date_input("Joining Date", datetime.now())

        submit_emp = st.form_submit_button("➕ Onboard Employee", type="primary")

        if submit_emp:
            if not emp_name or not emp_role:
                st.warning("Please fill in both Employee Name and Designation.")
            else:
                new_emp_id = f"EMP-{100 + len(st.session_state.admin_employees_db) + 1}"
                new_emp = pd.DataFrame([{
                    "Emp ID": new_emp_id,
                    "Employee Name": emp_name,
                    "Department": emp_dept,
                    "Role": emp_role,
                    "Joining Date": str(emp_date)
                }])
                st.session_state.admin_employees_db = pd.concat([st.session_state.admin_employees_db, new_emp], ignore_index=True)
                st.success(f"✅ Employee '{emp_name}' onboarded successfully with ID: {new_emp_id}")

    st.markdown("---")
    st.subheader("📋 Staff Directory")
    st.dataframe(st.session_state.admin_employees_db, use_container_width=True, hide_index=True)

# TAB 4: Manage Users
with tab4:
    st.subheader("User Authorization & Account Controls")
    st.write("Grant roles, modify access status, or reset credentials for registered user accounts.")

    st.dataframe(st.session_state.admin_users_db, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("⚙️ Update Account Access Status")
    
    u_col1, u_col2, u_col3 = st.columns(3)
    target_user = u_col1.selectbox("Select User Account", st.session_state.admin_users_db["Username"].tolist())
    new_role = u_col2.selectbox("Assign New Role", ["Super Admin", "Data Analyst", "Store Manager", "Standard User"])
    new_status = u_col3.selectbox("Set Account Status", ["Active", "Deactivated"])

    if st.button("🔄 Update User Privileges", type="primary"):
        idx = st.session_state.admin_users_db[st.session_state.admin_users_db["Username"] == target_user].index
        if not idx.empty:
            st.session_state.admin_users_db.loc[idx[0], "Role"] = new_role
            st.session_state.admin_users_db.loc[idx[0], "Status"] = new_status
            st.success(f"✅ User privileges updated for **{target_user}**! Role: `{new_role}`, Status: `{new_status}`.")
            st.rerun()
