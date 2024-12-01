import streamlit as st
from utils.api import (
    get_user_id,
    get_user_leagues,
    get_league_data,
    get_users,
    get_rosters,
)

st.set_page_config(layout="wide", page_title="Fantasy Football Dashboard")
st.title("Sleeper Fantasy Football Dashboard")
st.page_link("pages/historic_performance.py", label="View historic performance", icon="🏆")

st.markdown("""

This application helps you analyze your Sleeper fantasy football league performance across multiple seasons.

## Features

### Career Summary
- Track championships and regular season wins
- Monitor your success rate for making playoffs (Top 6)
- View average standings and performance metrics
- Track bottom 4 finishes

### Head-to-Head Analysis
- Compare your performance with other managers
- View detailed matchup history
- See win/loss records against specific opponents
- Track scoring differentials in matchups

### Performance Tracking
- Visualize your performance trends over time
- Compare your trajectory with other managers
- Track games above/below .500 across seasons
- See your performance across different leagues

## How to Use

1. Enter your Sleeper username in the text box
2. Use the year range slider to focus on specific seasons
3. Filter by specific leagues using the dropdown
4. Select another manager to view head-to-head comparisons

## Data Sources
All data is pulled directly from the Sleeper API and updates automatically throughout the season.

---
*Note: This tool only tracks leagues on the Sleeper platform and requires your leagues to be public.*
""")
