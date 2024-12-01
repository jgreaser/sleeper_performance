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
    
    # Display summary stats using a container for styling
    st.markdown(
        f"""
        <div style='padding: 20px; border-radius: 5px; background-color: #1E1E1E; margin-bottom: 20px;'>
            <div style='display: flex; justify-content: space-between; margin-bottom: 10px;'>
                <span style='color: white; font-weight: bold;'>Meetings total</span>
                <span style='color: white;'>{total_matchups}</span>
            </div>
            <div style='display: flex; justify-content: space-between;'>
                <span style='color: white; font-weight: bold;'>All-time series</span>
                <span style='color: white;'>{
                    f"{username} leads, {wins}–{losses}–{ties} ({(wins/total_matchups):.3f})" if wins > losses
                    else f"{selected_manager_name} leads, {losses}–{wins}–{ties} ({(losses/total_matchups):.3f})" if losses > wins
                    else f"Series tied, {wins}–{losses}–{ties}"
                }</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Create a display DataFrame
    display_df = matchup_df.copy()
    display_df['Score'] = display_df.apply(
        lambda x: f"{x['User Score']:.1f} - {x['Opponent Score']:.1f}", 
        axis=1
    )
    display_df['Diff'] = (display_df['User Score'] - display_df['Opponent Score']).abs().round(1)
    display_df['Winner'] = display_df.apply(
        lambda x: username if x['Result'] == 'Win' else selected_manager_name,
        axis=1
    )
    
    # Display the table using Streamlit's native table
    st.dataframe(
        display_df[['Season', 'Week', 'League', 'Score', 'Winner', 'Diff']],
        use_container_width=True,
        hide_index=True
    )