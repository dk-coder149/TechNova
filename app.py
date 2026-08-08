import streamlit as st
from db_connection import login_user, register_user

st.set_page_config(
    page_title="TechNova Analytics", page_icon="🚀", layout="wide"
)

# -------------------------------------------------------------
# GLOBAL THEME ENGINE
# -------------------------------------------------------------
def apply_global_theme():
    theme = st.session_state.get("theme_mode", "System Default 🖥️")
    
    if "Dark Mode" in theme:
        st.markdown("""
            <style>
                /* Main App Background */
                html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
                    background-color: #0E1117 !important;
                    color: #FAFAFA !important;
                }
                /* Sidebar */
                [data-testid="stSidebar"], [data-testid="stSidebarContent"] {
                    background-color: #161B22 !important;
                }
                /* Text Elements */
                p, h1, h2, h3, h4, h5, h6, span, label, td, th {
                    color: #FAFAFA !important;
                }
                /* Inputs & Dropdowns */
                input, textarea, select, div[data-baseweb="select"] {
                    background-color: #21262D !important;
                    color: #FAFAFA !important;
                }
                /* Cards, Forms & Dataframes */
                div[data-testid="stForm"], div[data-testid="stMetric"], .stDataFrame {
                    background-color: #161B22 !important;
                    border: 1px solid #30363D !important;
                    border-radius: 8px !important;
                }
            </style>
        """, unsafe_allow_html=True)

    elif "Light Mode" in theme:
        st.markdown("""
            <style>
                /* Main App Background */
                html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
                    background-color: #FFFFFF !important;
                    color: #111827 !important;
                }
                /* Sidebar */
                [data-testid="stSidebar"], [data-testid="stSidebarContent"] {
                    background-color: #F3F4F6 !important;
                }
                /* Text Elements */
                p, h1, h2, h3, h4, h5, h6, span, label, td, th {
                    color: #111827 !important;
                }
                /* Inputs & Dropdowns */
                input, textarea, select, div[data-baseweb="select"] {
                    background-color: #FFFFFF !important;
                    color: #111827 !important;
                }
                /* Cards, Forms & Dataframes */
                div[data-testid="stForm"], div[data-testid="stMetric"], .stDataFrame {
                    background-color: #F9FAFB !important;
                    border: 1px solid #E5E7EB !important;
                    border-radius: 8px !important;
                }
            </style>
        """, unsafe_allow_html=True)

# Function call taaki har page load par theme apply ho
apply_global_theme()


# -------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -------------------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = "User"


# -------------------------------------------------------------
# 1. LOGGED IN FLOW (Show Navigation & Analytics Pages)
# -------------------------------------------------------------
if st.session_state.logged_in:
    # Views folder se pages link karna
    dashboard = st.Page(
        "pages/1_Dashboard.py", title="Dashboard", icon="🏠", default=True
    )
    customers = st.Page("views/1_customers.py", title="Customers", icon="👥")
    products = st.Page("views/2_products.py", title="Products", icon="📦")
    orders = st.Page("views/3_orders.py", title="Orders", icon="🛒")
    sales = st.Page("views/4_sales.py", title="Sales", icon="📈")
    employees = st.Page("views/5_employees.py", title="Employees", icon="👨‍💼")
    inventory = st.Page("views/6_inventory.py", title="Inventory", icon="📋")

    reports = st.Page("views/9_reports.py", title="Reports Center", icon="📑")
    sql_lab = st.Page("views/10_sql_lab.py", title="SQL Query Lab", icon="💻")

    settings_page = st.Page("views/11_settings.py", title="Settings", icon="⚙️")
    admin_page = st.Page("views/12_admin.py", title="Admin Panel", icon="👑")
    
    # 🔒 Dynamic Management Pages based on Role
    management_pages = [settings_page]
    
    # KEVALL ADMIN LOGIN HONE PAR HI ADMIN PANEL ADD HOGA
    if st.session_state.get("role") == "Admin":
        management_pages.append(admin_page)

    # Complete Sidebar Navigation Tree
    pg = st.navigation(
        {
            "Main": [dashboard],
            "📊 Analytics": [
                customers,
                products,
                orders,
                sales,
                employees,
                inventory,
            ],
            "🧰 Tools": [reports, sql_lab],
            "⚙️ Management": management_pages
        }
    )

    # Logged-in User Info & Logout Button in Sidebar
    with st.sidebar:
        user_role = st.session_state.get("role", "User")
        role_icon = "👑 Admin" if user_role == "Admin" else "👤 User"
        
        st.write(
            f"👤 Logged in as: **{st.session_state.get('username', 'User')}**"
        )
        st.caption(f"Role: **{role_icon}**")
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            st.session_state.logged_in = False
            st.session_state.role = "User"
            st.rerun()  # Refresh app to show login page

    # Selected view page run karna
    pg.run()


# -------------------------------------------------------------
# 2. LOGGED OUT FLOW (Public Landing Page + Login / Signup)
# -------------------------------------------------------------
else:
    # PUBLIC SIDEBAR (Login / Signup Forms)
    st.sidebar.title("🔐 Access Portal")

    auth_choice = st.sidebar.radio(
        "Choose Action", ["Login", "Sign Up"], key="public_auth_radio"
    )

    if auth_choice == "Login":
        st.sidebar.subheader("Login to Account")
        username = st.sidebar.text_input(
            "Username / Email", key="public_login_user"
        )
        password = st.sidebar.text_input(
            "Password", type="password", key="public_login_pass"
        )

        if st.sidebar.button(
            "Login",
            type="primary",
            use_container_width=True,
            key="btn_pub_login",
        ):
            if username and password:
                if login_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    
                    # 👑 ROLE ASSIGNMENT: Checking if User is Admin
                    if username.lower() in ["admin", "admin@technova.com"]:
                        st.session_state.role = "Admin"
                    else:
                        st.session_state.role = "User"

                    st.sidebar.success("Login Successful!")
                    st.rerun()  # Re-evaluate app state to open Dashboard
                else:
                    st.sidebar.error("Invalid credentials!")
            else:
                st.sidebar.warning("Fill all fields.")

    elif auth_choice == "Sign Up":
        st.sidebar.subheader("Create New Account")
        new_user = st.sidebar.text_input(
            "Username / Email", key="public_reg_user"
        )
        new_pass = st.sidebar.text_input(
            "Password", type="password", key="public_reg_pass"
        )
        confirm_pass = st.sidebar.text_input(
            "Confirm Password", type="password", key="public_reg_confirm"
        )

        if st.sidebar.button(
            "Register",
            type="primary",
            use_container_width=True,
            key="btn_pub_signup",
        ):
            if new_user and new_pass and confirm_pass:
                if new_pass == confirm_pass:
                    if register_user(new_user, new_pass):
                        st.sidebar.success(
                            "Account created! Please switch to Login."
                        )
                    else:
                        st.sidebar.error("Username already exists!")
                else:
                    st.sidebar.error("Passwords do not match!")
            else:
                st.sidebar.warning("Fill all fields.")

    # PUBLIC MAIN PAGE (Information Area)
    st.title("📊 TechNova Enterprise Retail Analytics")
    st.info(
        "👉 Please **Login** or **Sign Up** from the Sidebar on the left to access full analytics and reports."
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        #### 🚀 Key Features:
        * **Real-time Sales & Profit Analytics**
        * **State-wise & Category-wise Breakdown**
        * **Customer RFM Analysis & VIP Tracking**
        * **Low Inventory Warning & Automated Alerts**
        """)
    with col2:
        st.image(
            "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800",
            caption="Enterprise Analytics Preview",
        )