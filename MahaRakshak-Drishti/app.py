import streamlit as st
from src.auth import login_officer, login_citizen, check_login_status

# --- INITIALIZATION ---
check_login_status()
st.set_page_config(page_title="MahaRakshak-Drishti | Gateway", layout="wide")

# --- PROFESSIONAL STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; }
    .hero-section {
        background: linear-gradient(135deg, #1E1B4B 0%, #3730A3 100%);
        padding: 60px 40px; border-radius: 25px; color: white; text-align: center;
        margin-bottom: 40px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .feature-card {
        background: white; padding: 25px; border-radius: 15px;
        border: 1px solid #E2E8F0; height: 100%;
    }
    h1 { color: #F1F5F9 !important; font-weight: 800 !important; }
    h3 { color: #1E293B !important; margin-top: 0; }
    </style>
    """, unsafe_allow_html=True)

# --- HERO LANDING ---
st.markdown("""
    <div class="hero-section">
        <h1>🛡️ MahaRakshak-Drishti</h1>
        <p style='font-size: 1.2rem; color: #C7D2FE;'>Maharashtra State Advanced Crime Intelligence & Digital Governance Portal</p>
    </div>
    """, unsafe_allow_html=True)

# --- APP INFORMATION ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="feature-card">
            <h3>🏛️ Executive Mission</h3>
            <p>Providing a data-driven tactical edge to law enforcement through real-time geospatial analytics 
            and predictive crime monitoring to ensure statewide security.</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <h3>📢 Public Empowerment</h3>
            <p>Fostering transparency by providing citizens with localized safety insights and a 
            secure, bilingual digital channel for reporting non-emergency incidents.</p>
        </div>
        """, unsafe_allow_html=True)

# --- SIDEBAR AUTHENTICATION PORTAL ---
with st.sidebar:
    st.image("static/logo.png", use_container_width=True)
    st.markdown("## 🔐 Secure Access")
    
    # OFFICER LOGIN SECTION
    with st.expander("👮 Officer Personnel"):
        u = st.text_input("Personnel ID")
        p = st.text_input("Access Key", type="password")
        if st.button("Verify Credentials", use_container_width=True):
            if login_officer(u, p):
                st.success("Authentication Successful")
                st.switch_page("pages/1_📡_Tactical_Hub.py")
            else:
                st.error("Invalid Personnel ID or Key")

    st.divider()
    
    # CITIZEN LOGIN SECTION
    st.markdown("### 👤 Public Portal")
    if st.button("Enter as Citizen", use_container_width=True):
        login_citizen()
        st.switch_page("pages/4_📢_Citizen_Portal.py")

    st.sidebar.warning("🚨 Emergency? Dial 112")