import streamlit as st
import pandas as pd

def display_head_to_head_summary(username, selected_manager_name, matchup_df):
    """Display head-to-head matchup summary"""
    st.subheader("Head-to-Head History")
    
    if matchup_df.empty:
        st.write("No head-to-head matchups found")
        return

    total_matchups = len(matchup_df)
    wins = len(matchup_df[matchup_df['Result'] == 'Win'])
    losses = len(matchup_df[matchup_df['Result'] == 'Loss'])
    ties = len(matchup_df[matchup_df['Result'] == 'Tie'])
    
    # Display summary stats
    st.markdown("""
        <div style="background-color: #1E1E1E; padding: 20px; border-radius: 5px; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span style="font-weight: bold; color: #FFFFFF;">Meetings total</span>
                <span style="color: #FFFFFF;">{}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span style="font-weight: bold; color: #FFFFFF;">All-time series</span>
                <span style="color: #FFFFFF;">{}</span>
            </div>
        </div>
    """.format(
        total_matchups,
        f"{username} leads, {wins}–{losses}–{ties} ({(wins/total_matchups):.3f})" if wins > losses else
        f"{selected_manager_name} leads, {losses}–{wins}–{ties} ({(losses/total_matchups):.3f})" if losses > wins else
        f"Series tied, {wins}–{losses}–{ties}"
    ), unsafe_allow_html=True)