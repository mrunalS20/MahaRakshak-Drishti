import streamlit as st

def check_login_status():
    """
    Initializes session states to prevent 'KeyError' when navigating.
    """
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None

def login_officer(username, password):
    """
    Validates credentials for the Maharashtra State Intelligence Unit.
    """
    # Standard credentials for the prototype phase
    if username == "admin" and password == "police123":
        st.session_state.logged_in = True
        st.session_state.user_role = "Officer"
        return True
    return False

def login_citizen():
    """
    Sets the session role to 'Citizen' for public portal access.
    """
    st.session_state.logged_in = True
    st.session_state.user_role = "Citizen"

def logout():
    """
    Resets session state and returns user to the home gateway.
    """
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.rerun()

def require_officer():
    """
    Security Middleware: Add to the top of all restricted personnel pages.
    """
    check_login_status()
    if st.session_state.user_role != "Officer":
        st.error("🚫 Access Restricted: This module is for authorized personnel only.")
        if st.button("Return to Gateway"):
            st.switch_page("app.py")
        st.stop()