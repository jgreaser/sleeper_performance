# utils/nfl_calendar.py
import requests 
import streamlit as st
from datetime import datetime, timezone
from typing import Tuple

def get_current_nfl_week() -> Tuple[str, str, int]:
    today = datetime.now()
    st.sidebar.info(f"Today's date: {today.strftime('%Y-%m-%d')}")
    
    try:
        response = requests.get("https://api.nfl.com/v3/shield/?query=query%7Bviewer%7Bcurrent%7Bweek%7D%7D%7D",
                              headers={"Client-ID": "d5c67b30-6f1d-451e-9bcd-dc4da919f973"})
        if response.status_code == 200:
            week = response.json()['data']['viewer']['current']['week']
            st.sidebar.info(f"NFL API: Week {week}, Year {today.year}")
            return str(today.year), 'regular', week
    except Exception as e:
        st.sidebar.warning(f"NFL API Error: {str(e)}")
    
    # Fallback calculation for 2024 season (starts Sept 5, 2024)
    season_start = datetime(2024, 9, 5)
    if today >= season_start:
        week = ((today - season_start).days // 7) + 1
    else:
        week = 12  # Current week as of Nov 25, 2024
        
    st.sidebar.warning(f"Using fallback: Week {week}, Year {today.year}")
    return str(today.year), 'regular', week
