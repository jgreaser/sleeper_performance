import streamlit as st
import pandas as pd

def display_head_to_head_summary(username, selected_manager_name, matchup_df):
    """Display head-to-head matchup summary"""
    st.subheader("Head-to-Head History")
    
    if matchup_df.empty:
        st.write("No head-to-head matchups found")
        return

    # Filter out incomplete matchups
    complete_matchups = matchup_df[
        ~((matchup_df['User Score'] == 0) | (matchup_df['Opponent Score'] == 0))
    ]
    
    if complete_matchups.empty:
        st.write("No completed matchups found")
        return

    # Calculate stats
    total_matchups = len(complete_matchups)
    wins = len(complete_matchups[complete_matchups['Result'] == 'Win'])
    losses = len(complete_matchups[complete_matchups['Result'] == 'Loss'])
    ties = len(complete_matchups[complete_matchups['Result'] == 'Tie'])
    
    # Calculate series text
    if wins > losses:
        series_text = f"{username} leads"
        record = f"{wins}–{losses}–{ties} ({(wins/total_matchups):.3f})"
    elif losses > wins:
        series_text = f"{selected_manager_name} leads"
        record = f"{losses}–{wins}–{ties} ({(losses/total_matchups):.3f})"
    else:
        series_text = "Series tied"
        record = f"{wins}–{losses}–{ties}"
    
    # Display summary stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.caption("Meetings total")
        st.subheader(str(total_matchups))
        
    with col2:
        st.caption("All-time series")
        st.subheader(series_text)
        st.text(record)
    
    # Calculate playoff record if Type column exists
    if 'Type' in complete_matchups.columns:
        playoff_df = complete_matchups[complete_matchups['Type'].str.contains('Playoffs', na=False)]
        if not playoff_df.empty:
            playoff_wins = len(playoff_df[playoff_df['Result'] == 'Win'])
            playoff_losses = len(playoff_df[playoff_df['Result'] == 'Loss'])
            with col3:
                st.caption("Playoff record 🏆")
                st.subheader(f"{playoff_wins}–{playoff_losses}")
    
    st.write("")
    st.write("Matchup History")
    
    # Create a display DataFrame
    display_df = complete_matchups.copy()
    display_df['Score'] = display_df.apply(
        lambda x: f"{x['User Score']:.1f} - {x['Opponent Score']:.1f}", 
        axis=1
    )
    display_df['Diff'] = (display_df['User Score'] - display_df['Opponent Score']).abs().round(1)
    display_df['Winner'] = display_df.apply(
        lambda x: username if x['Result'] == 'Win' else selected_manager_name,
        axis=1
    )
    
    # Add playoff indicator to league name if it's a playoff game
    if 'Type' in display_df.columns:
        display_df['League'] = display_df.apply(
            lambda x: f"{x['League']} 🏆" if 'Playoffs' in str(x.get('Type', '')) else x['League'],
            axis=1
        )
    
    # Convert Season to string to prevent comma formatting
    display_df['Season'] = display_df['Season'].astype(str)
    
    # Prepare display columns and sort
    display_columns = ['Season', 'Week', 'League', 'Score', 'Winner', 'Diff']
    display_df = display_df.sort_values(['Season', 'Week'], ascending=[False, True])
    
    # Display the table
    st.dataframe(
        display_df[display_columns],
        use_container_width=True,
        hide_index=True
    )