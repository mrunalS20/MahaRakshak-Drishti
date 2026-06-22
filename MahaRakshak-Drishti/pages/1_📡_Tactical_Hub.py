import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
from src.data_loader import load_and_clean_data
from src.auth import require_officer

# --- SECURITY GATE ---
# Prevents citizens from accessing this page via direct URL
require_officer() 

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Tactical Hub | MRD", layout="wide")

# --- HIGH-CONTRAST TACTICAL UI ---
st.markdown("""
    <style>
    /* Professional Background & Typography */
    .stApp { background-color: #F8FAFC; font-family: 'Inter', sans-serif; }
    
    /* Heading Visibility */
    h1, h4 { color: #0F172A !important; font-weight: 800 !important; }
    
    /* Section Headers with Indigo Accent */
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

    /* Strategic Overview Card */
    .overview-card {
        background: white; 
        padding: 24px; 
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .overview-card p { color: #64748B; font-weight: 500; margin-bottom: 0; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>📡 Tactical Command Center</h1>", unsafe_allow_html=True)

try:
    # 1. Load Statewide Data
    df = load_and_clean_data("data/raw_crime_data.csv")

    # --- TACTICAL VALUE: HOURLY FREQUENCY ANALYSIS ---
    st.markdown("<div class='section-header'>Strategic Patrol Intelligence</div>", unsafe_allow_html=True)
    
    # Ensure Timestamp is datetime and extract hour for the chart
    df['Hour'] = df['Timestamp'].dt.hour
    hour_counts = df.groupby('Hour').size().reindex(range(0, 24), fill_value=0)

    with st.container():
        st.markdown(f"""
            <div class='overview-card'>
                <h4 style='margin:0;'>📊 24-Hour Crime Distribution</h4>
                <p>Tactical Insight: Peak activity detected at <b>{hour_counts.idxmax()}:00 HRS</b>. 
                Adjust patrol shifts to accommodate high-frequency windows.</p>
            </div>
        """, unsafe_allow_html=True)
        # Wide Bar Chart for shift decision support
        st.bar_chart(hour_counts, color="#6366F1")

    st.divider()

    # --- GEOSPATIAL & REAL-TIME FEED ---
    col_map, col_feed = st.columns([2, 1])

    with col_map:
        st.markdown("<div class='section-header'>Live Heat Radar</div>", unsafe_allow_html=True)
        # Center on Maharashtra
        m = folium.Map(location=[19.7506, 75.7139], zoom_start=6, tiles="cartodbpositron")
        
        # Overlay Crime Density
        HeatMap([[r['Latitude'], r['Longitude']] for _, r in df.iterrows()], 
                radius=15, blur=18).add_to(m)
        
        st_folium(m, width="100%", height=500)

    with col_feed:
        st.markdown("<div class='section-header'>Live Dispatch Feed</div>", unsafe_allow_html=True)
        # Display the most recent 10 incidents for immediate review
        recent_logs = df[['Timestamp', 'Crime_Type', 'Police_Station']].sort_values('Timestamp', ascending=False).head(10)
        st.dataframe(recent_logs, use_container_width=True, hide_index=True)
        
        st.info("💡 **Tip:** Frequent theft clusters in specific sectors may require SRPF deployment.")

except Exception as e:
    st.error(f"⚠️ Tactical Intelligence Sync Failed: {e}")