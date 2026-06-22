import streamlit as st
from src.data_loader import load_and_clean_data
from src.zoning_engine import calculate_risk_zones
from src.auth import require_officer

# --- SECURITY GATE ---
# Ensures only personnel with 'Officer' role can access tactical SOPs
require_officer() 

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Safety Protocols | MRD", layout="wide")

# --- HIGH-CONTRAST PROFESSIONAL UI ---
st.markdown("""
    <style>
    /* Global App Background */
    .stApp { background-color: #F8FAFC; font-family: 'Inter', sans-serif; }
    
    /* VISIBILITY FOR HEADINGS */
    h1, h2, h3 { 
        color: #0F172A !important; 
        font-weight: 800 !important; 
        opacity: 1 !important;
        margin-bottom: 1.2rem !important;
    }
    
    /* SECTION HEADER STYLE */
    .section-header {
        color: #1E293B !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        border-left: 5px solid #4F46E5;
        padding-left: 15px;
        margin: 25px 0 15px 0 !important;
        text-transform: uppercase;
        letter-spacing: 0.02em;
    }

    /* PROTOCOL ALERT BOXES */
    .protocol-card {
        background: white; padding: 25px; border-radius: 15px;
        border-top: 6px solid #EF4444; margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-left: 1px solid #E2E8F0;
        border-right: 1px solid #E2E8F0;
        border-bottom: 1px solid #E2E8F0;
    }
    .protocol-card b { color: #0F172A !important; }
    </style>
    """, unsafe_allow_html=True)

try:
    # 1. Load and Process Data
    df = load_and_clean_data("data/raw_crime_data.csv")
    risk_df = calculate_risk_zones(df)

    # 2. Main Header
    st.markdown("<h1>🛡️ Strategic Safety Protocols</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #475569; font-size: 1.1rem;'>Automated decision support for high-risk jurisdictions in Maharashtra.</p>", unsafe_allow_html=True)

    # 3. Risk-Based Interventions
    high_risk_regions = risk_df[risk_df['Risk_Level'].str.contains("High")]

    if not high_risk_regions.empty:
        st.markdown("<div class='section-header'>Active High-Risk Deployments</div>", unsafe_allow_html=True)
        
        for _, region in high_risk_regions.iterrows():
            with st.expander(f"🚨 ALERT: {region['Police_Station']} HQ", expanded=True):
                col_info, col_sop = st.columns([1, 2])
                
                with col_info:
                    st.markdown(f"""
                        <div style='padding: 15px; background: #FFF1F2; border-radius: 10px; border: 1px solid #FECDD3;'>
                            <b style='color: #9F1239;'>RISK LEVEL: {region['Risk_Level']}</b><br>
                            <span style='color: #BE123C; font-size: 0.9rem;'>Incident Load: {region['incident_count']} Reports</span>
                        </div>
                    """, unsafe_allow_html=True)
                    st.info("Tactical recommendation based on real-time frequency spikes.")

                with col_sop:
                    st.markdown("<b>Mandatory Tactical SOPs:</b>", unsafe_allow_html=True)
                    st.write("*   **Patrol Surge:** Deploy 2 extra mobile units for night patrol (22:00 - 04:00 HRS).")
                    st.write("*   **Nakabandi:** Establish highway checkpoints at all major entry/exit points.")
                    st.write("*   **Public Alert:** Broadcast safety advisories via JanSetu localized nodes.")
    else:
        st.success("✅ Operational Status: Nominal. No statewide emergency protocols triggered.")

    # 4. Standard Operating Procedures (SOPs)
    st.divider()
    st.markdown("<div class='section-header'>Statewide Standard Operating Procedures</div>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
            <div class='protocol-card'>
                <h4>💻 Cyber Response</h4>
                <p style='color: #334155;'>Coordinate with Maharashtra Cyber Cell for immediate account freezing and takedowns.</p>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
            <div class='protocol-card' style='border-top-color: #6366F1;'>
                <h4>📢 Civil Unrest</h4>
                <p style='color: #334155;'>Mobilize Rapid Action Force (RAF) and monitor social media for rumor control.</p>
            </div>
        """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Failed to synchronize safety protocols: {e}")