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
