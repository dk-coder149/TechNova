import streamlit as st
from db_connection import login_user, register_user

st.set_page_config(page_title="Auth - TechNova", page_icon="🔐")

# -------------------------------------------------------------
# 1. Page State Management (Login/Signup toggle karne ke liye)
# -------------------------------------------------------------
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"


def set_mode(mode):
    st.session_state.auth_mode = mode


# -------------------------------------------------------------
# 2. LOGIN FORM VIEW
# -------------------------------------------------------------
if st.session_state.auth_mode == "login":
    st.title("Welcome Back 👋")
    st.subheader("Login to your account")

    username = st.text_input(
        "Username / Email", placeholder="username@email.com", key="login_user"
    )
    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter password",
        key="login_pass",
    )

    if st.button("Login", type="primary", use_container_width=True):
        if username and password:
            if login_user(username, password):
                st.success("Login Successful 🎉")
                # Yahan aap login hone ke baad dashboard page par switch kar sakte hain:
                # st.switch_page("pages/2_dashboard.py")
            else:
                st.error("Invalid Username or Password!")
        else:
            st.warning("Please fill in both fields.")

    st.divider()

    # Signup Toggle
    st.markdown(
        "<p style='text-align: center; margin-bottom: 5px;'>Don't have an account?</p>",
        unsafe_allow_html=True,
    )
    st.button(
        "📝 Create New Account",
        use_container_width=True,
        on_click=set_mode,
        args=("signup",),
    )


# -------------------------------------------------------------
# 3. SIGNUP FORM VIEW
# -------------------------------------------------------------
elif st.session_state.auth_mode == "signup":
    st.title("Create Account 🚀")
    st.subheader("Register a new user")

    new_username = st.text_input(
        "Username / Email", placeholder="username@email.com", key="reg_user"
    )
    new_password = st.text_input(
        "Password",
        type="password",
        placeholder="Create password",
        key="reg_pass",
    )
    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        placeholder="Confirm password",
        key="reg_confirm_pass",
    )

    if st.button("Sign Up", type="primary", use_container_width=True):
        if new_username and new_password and confirm_password:
            if new_password == confirm_password:
                if register_user(new_username, new_password):
                    st.success(
                        "Account created successfully! Redirecting to login..."
                    )
                    # Successful registration ke baad auto-switch to Login
                    st.session_state.auth_mode = "login"
                    st.rerun()
                else:
                    st.error("Username already exists!")
            else:
                st.error("Passwords do not match!")
        else:
            st.warning("Please fill all fields.")

    st.divider()

    # Back to Login Toggle
    st.markdown(
        "<p style='text-align: center; margin-bottom: 5px;'>Already have an account?</p>",
        unsafe_allow_html=True,
    )
    st.button(
        "⬅️ Back to Login",
        use_container_width=True,
        on_click=set_mode,
        args=("login",),
    )