import streamlit as st
from datetime import datetime
from src.data_loader import load_and_clean_data

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Citizen Portal | MRD", layout="wide")

# --- HIGH-CONTRAST PROFESSIONAL UI ---
st.markdown("""
    <style>
    /* Global App Background */
    .stApp { background-color: #F8FAFC; font-family: 'Inter', sans-serif; }
    
    /* VISIBILITY FOR HEADINGS */
    h1, h3 { 
        color: #0F172A !important; 
        font-weight: 800 !important; 
        margin-bottom: 1.2rem !important;
    }
    
    /* SECTION HEADER STYLE */
    .section-header {
        color: #1E293B !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        border-left: 5px solid #4F46E5;
        padding-left: 15px;
        margin: 25px 0 !important;
        text-transform: uppercase;
        letter-spacing: 0.02em;
    }

    /* COMPLAINT FORM BOX */
    .complaint-container {
        background: white; 
        padding: 30px; 
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    </style>
    """, unsafe_allow_html=True)

try:
    # 1. Page Header
    st.markdown("<h1>📢 Citizen Reporting & Public Safety</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #475569; font-size: 1.1rem; margin-bottom: 30px;'>Empowering the residents of Maharashtra with transparency and secure digital reporting tools.</p>", unsafe_allow_html=True)

    # 2. Public Data Transparency
    st.markdown("<div class='section-header'>Statewide Crime Transparency</div>", unsafe_allow_html=True)
    df = load_and_clean_data("data/raw_crime_data.csv")
    
    col_chart, col_info = st.columns([2, 1])
    
    with col_chart:
        # Visualizing real crime rates to build community awareness
        crime_rates = df['Crime_Type'].value_counts()
        st.bar_chart(crime_rates, color="#4F46E5")
    
    with col_info:
        st.info("**Community Impact**\n\nPublicly sharing incident data helps citizens identify high-risk zones and assists local authorities in justifying safety improvements like better street lighting.")
        st.metric("Total Documented Incidents", len(df))

    st.divider()

    # 3. Digital Complaint Management System
    st.markdown("<div class='section-header'>Submit a Secure Digital Complaint</div>", unsafe_allow_html=True)
    st.write("Use this portal to report non-emergency incidents directly to the Maharashtra State Intelligence Unit. For immediate danger, always call **112**.")

    with st.container():
        with st.form("citizen_complaint_form", clear_on_submit=True):
            f_col1, f_col2 = st.columns(2)
            
            with f_col1:
                c_type = st.selectbox("Incident Type", [
                    "Theft", "Cyber Fraud", "Harassment", "Vandalism", "Other"
                ])
                c_loc = st.text_input("Area / District (e.g., Kothrud, Pune)")
            
            with f_col2:
                c_date = st.date_input("Date of Incident", value=datetime.now())
                c_contact = st.text_input("Contact Number (Optional)")

            c_desc = st.text_area("Detailed Narrative", placeholder="Please provide a clear description of the event...")
            
            # Submit button with primary branding
            submitted = st.form_submit_button("Submit Secure Report", use_container_width=True)
            
            if submitted:
                if c_loc and c_desc:
                    # Logic to save to data/complaints.csv would be integrated here
                    ref_id = f"MRD-REF-{datetime.now().strftime('%S%f')[:4]}"
                    st.success(f"Complaint successfully filed. Reference ID: **{ref_id}**")
                    st.balloons()
                    st.info("Your report has been securely logged for preliminary review by the district intelligence cell.")
                else:
                    st.error("Submission Failed: Please provide both the location and description of the incident.")

except Exception as e:
    st.error(f"Portal Connectivity Error: {e}")

# Sidebar Emergency Branding
with st.sidebar:
    st.image("static/logo.png", use_container_width=True)
    st.markdown("<h2 style='text-align: center; color: white;'>PUBLIC SAFETY</h2>", unsafe_allow_html=True)
    st.error("🚨 EMERGENCY: CALL 112")
    st.divider()
    st.write("**Public Guidelines:**")
    st.write("1. Filing false reports is a punishable offense.")
    st.write("2. Ensure locations are as specific as possible.")
    st.write("3. This portal is for non-emergency intelligence gathering.")