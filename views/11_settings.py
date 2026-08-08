import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")
st.title("⚙️ System & User Settings")
st.caption("Manage your account details, security preferences, and application appearance.")

# Get current user from session state
current_username = st.session_state.get("username", "Admin")

tab1, tab2, tab3, tab4 = st.tabs([
    "👤 User Profile", 
    "🔑 Change Password", 
    "🎨 Appearance & Theme", 
    "🚪 Logout & Session"
])

# TAB 1: User Profile
with tab1:
    st.subheader("User Profile Details")
    st.write("View and update your personal user profile information.")

    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Username", value=current_username, disabled=True, help="Username cannot be changed.")
        email_val = st.text_input("Email Address", value=f"{current_username.lower().replace(' ', '.')}@technova.com")
        phone_val = st.text_input("Phone Number", value="+91 98765 43210")

    with col2:
        st.text_input("Role / Permission Level", value="Administrator", disabled=True)
        st.text_input("Department", value="Analytics & Business Intelligence")
        st.text_input("Account Created On", value="2026-01-10", disabled=True)

    if st.button("💾 Save Profile Changes", type="primary"):
        st.success("✅ Profile details updated successfully!")

# TAB 2: Change Password
with tab2:
    st.subheader("Update Account Password")
    st.caption("Ensure your account uses a strong password with at least 6 characters.")

    with st.form("change_password_form", clear_on_submit=True):
        current_pass = st.text_input("Current Password", type="password")
        new_pass = st.text_input("New Password", type="password")
        confirm_pass = st.text_input("Confirm New Password", type="password")

        submit_pass = st.form_submit_button("🚀 Change Password", type="primary")

        if submit_pass:
            if not current_pass or not new_pass or not confirm_pass:
                st.warning("Please fill in all password fields.")
            elif new_pass != confirm_pass:
                st.error("❌ New password and confirm password do not match!")
            elif len(new_pass) < 6:
                st.warning("⚠️ New password must be at least 6 characters long.")
            else:
                st.success("✅ Password updated successfully!")

# TAB 3: Theme & Preferences
with tab3:
    st.subheader("Interface & System Preferences")

    current_theme = st.session_state.get("theme_mode", "System Default 🖥️")
    theme_options = ["System Default 🖥️", "Light Mode ☀️", "Dark Mode 🌙"]
    
    selected_idx = theme_options.index(current_theme) if current_theme in theme_options else 0

    theme_mode = st.radio(
        "Choose Preferred UI Theme",
        theme_options,
        index=selected_idx,
        horizontal=True
    )

    st.markdown("---")

    if st.button("⚙️ Save & Apply Theme", type="primary"):
        st.session_state["theme_mode"] = theme_mode
        st.success(f"✅ Theme set to '{theme_mode}'")
        st.rerun()

               
# TAB 4: Logout
with tab4:
    st.subheader("End Active Session")
    st.write("Logging out will safely terminate your session and return you to the login screen.")

    st.warning("Make sure any unsaved query or report configurations are downloaded before logging out.")
    
    col_out1, col_out2 = st.columns([1, 4])
    with col_out1:
        if st.button("🚪 Logout Now", type="secondary", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()