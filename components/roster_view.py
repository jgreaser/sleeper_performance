import streamlit as st
import pandas as pd
from utils.data_processing import create_roster_df

def display_roster(users_df, rosters, players_data, weekly_stats):
    selected_user = st.selectbox(
        "Select Player",
        users_df['Display Name'].tolist()
    )
    
    if selected_user:
        user_id = users_df[users_df['Display Name'] == selected_user]['user_id'].iloc[0]
        roster = next((r for r in rosters if r['owner_id'] == user_id), None)
        
        if roster:
            roster_df = create_roster_df(roster, players_data, weekly_stats)
            if not roster_df.empty:
                st.dataframe(roster_df)
                
                selected_player_name = st.selectbox(
                    "Select Player for Stats",
                    roster_df['Name'].tolist()
                )
                
                if selected_player_name:
                    return roster_df[roster_df['Name'] == selected_player_name].iloc[0].to_dict()
    return None