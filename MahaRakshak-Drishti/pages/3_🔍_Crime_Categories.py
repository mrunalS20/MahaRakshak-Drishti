import streamlit as st
from src.data_loader import load_and_clean_data

# --- PAGE CONFIG ---
st.set_page_config(page_title="Crime Encyclopedia | MRD", layout="wide")

# --- HIGH-CONTRAST UI ---
st.markdown("""
    <style>
    /* Global App Background */
    .stApp { background-color: #F8FAFC; font-family: 'Inter', sans-serif; }
    
    /* VISIBILITY FOR HEADINGS */
    h1 { color: #0F172A !important; font-weight: 800 !important; margin-bottom: 1.5rem !important; }
    
    /* ENCYCLOPEDIA CARD */
    .cat-card {
        background: white; padding: 30px; border-radius: 16px;
        border-left: 8px solid #4F46E5; border-right: 1px solid #E2E8F0;
        border-top: 1px solid #E2E8F0; border-bottom: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 30px;
    }
    .cat-card h3 { color: #4F46E5 !important; margin-top: 0; }
    .cat-card p { color: #334155 !important; font-size: 1.1rem !important; line-height: 1.6; font-weight: 500; }
    </style>
    """, unsafe_allow_html=True)

# --- CRIME DATABASE ---
CRIME_DB = {
    "Theft": "Unauthorized taking of property with intent to deprive the owner permanently. Includes vehicle theft and shoplifting.",
    "Cyber Crime": "Criminal activities carried out via computers or the internet, including phishing, online fraud, and hacking.",
    "Assault": "A physical attack or a threat of physical attack on another person.",
    "Fraud": "Deception intended to result in financial or personal gain, often involving marketplace transactions.",
    "Vandalism": "Intentional destruction or damage to public or private property."
}

st.markdown("<h1>🔍 Crime Category Encyclopedia</h1>", unsafe_allow_html=True)

try:
    # 1. Load Statewide Data
    df = load_and_clean_data("data/raw_crime_data.csv")

    # 2. Interactive Analysis Layout
    col_sel, col_stat = st.columns([1.2, 1])

    with col_sel:
        st.markdown("### Select Category for Analysis")
        category = st.selectbox("Choose a Crime Type", list(CRIME_DB.keys()), label_visibility="collapsed")
        
        # Display high-contrast definition card
        st.markdown(f"""
            <div class="cat-card">
                <h3>{category}</h3>
                <p>{CRIME_DB[category]}</p>
            </div>
        """, unsafe_allow_html=True)

    with col_stat:
        st.markdown("### Statewide Statistics")
        # Filter data for specific category frequency
        category_df = df[df['Crime_Type'] == category]
        count = len(category_df)
        
        st.metric(f"Total {category} Incidents", count)
        
        # Tactical insight for officers vs awareness for citizens
        st.info(f"**Strategic Insight:** {category} patterns show regional variance across Maharashtra districts. "
                "Refer to the Tactical Hub for specific geospatial clusters and time-of-day peak analysis.")

except Exception as e:
    st.error(f"Encyclopedia Sync Error: {e}")