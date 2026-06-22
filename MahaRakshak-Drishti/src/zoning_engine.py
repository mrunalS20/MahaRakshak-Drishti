import pandas as pd

def calculate_risk_zones(df):
    """
    Categorizes police jurisdictions into Low, Medium, or High risk 
    based on incident density to guide resource allocation.
    """
    if df.empty:
        return pd.DataFrame()

    # 1. Group incidents by Police Station to determine density
    stats = df.groupby('Police_Station').size().reset_index(name='incident_count')
    
    # 2. Define Tactical Risk Thresholds
    # These thresholds determine when high-priority SOPs are triggered
    def assign_risk(count):
        if count > 10: 
            return "🔴 High Risk"
        if count > 5:  
            return "🟡 Medium Risk"
        return "🟢 Low Risk"

    # 3. Apply risk classification
    stats['Risk_Level'] = stats['incident_count'].apply(assign_risk)
    
    # Sort by count so high-priority areas appear first in tactical lists
    stats = stats.sort_values(by='incident_count', ascending=False)
    
    return stats