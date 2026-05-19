import streamlit as st
from utils.auth import sign_in, sign_up

def show_login_page():
    st.title("🧠 AI Mental Health Journal")
    st.write("Your safe space to journal and track your emotional wellbeing.")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    # Login tab
    with tab1:
        st.subheader("Welcome back!")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", use_container_width=True):
            if email and password:
                user, error = sign_in(email, password)
                if user:
                    st.session_state.user = user
                    st.success("Logged in successfully! ✅")
                    st.rerun()
                else:
                    st.error(f"Login failed: {error}")
            else:
                st.warning("Please fill in all fields")

    # Sign up tab
    with tab2:
        st.subheader("Create an account")
        full_name = st.text_input("Full Name", key="signup_name")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm")

        if st.button("Sign Up", use_container_width=True):
            if full_name and email and password and confirm_password:
                if password != confirm_password:
                    st.error("Passwords do not match!")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters!")
                else:
                    user, error = sign_up(email, password, full_name)
                    if user:
                        st.success("Account created! Please check your email to verify your account ✅")
                    else:
                        st.error(f"Sign up failed: {error}")
            else:
                st.warning("Please fill in all fields")