import streamlit as st
from views.login import show_login_page
from views.journal import show_journal_page
from views.dashboard import show_dashboard_page
from views.weekly_summary import show_weekly_summary_page

st.set_page_config(
    page_title="AI Mental Health Journal",
    page_icon="🧠",
    layout="wide"
)

if "user" not in st.session_state:
    show_login_page()
else:
    user = st.session_state.user

    with st.sidebar:
        st.title("🧠 AI Journal")
        st.write(f"👋 Welcome!")
        st.divider()
        page = st.radio("Navigate", [
            "📝 Journal",
            "📊 Dashboard",
            "💬 Weekly Summary"
        ])
        st.divider()
        if st.button("Logout", use_container_width=True):
            del st.session_state.user
            st.rerun()

    if page == "📝 Journal":
        show_journal_page(user)
    elif page == "📊 Dashboard":
        show_dashboard_page(user)
    elif page == "💬 Weekly Summary":
        show_weekly_summary_page(user)