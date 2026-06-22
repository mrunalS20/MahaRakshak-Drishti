import pandas as pd
import streamlit as st

@st.cache_data
def load_and_clean_data(file_path):
    """
    Loads raw crime data and ensures timestamps are formatted for 
    time-series and hourly analysis.
    """
    try:
        # Load the dataset from the data directory
        df = pd.read_csv(file_path)
        
        # ESSENTIAL STEP: Convert Timestamp to datetime objects
        # This allows the Tactical Hub to extract the .hour property for frequency charts
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        
        # Remove any leading/trailing whitespace from categorical columns
        for col in ['Crime_Type', 'Police_Station']:
            if col in df.columns:
                df[col] = df[col].str.strip()
                
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()