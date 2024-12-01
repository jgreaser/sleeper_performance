import streamlit as st
import pandas as pd

def display_matchup_table(matchup_df, username, selected_manager_name):
    """Display the game results table with improved formatting."""
    
    # Add table styles for Wikipedia-like feel
    st.markdown("""
        <style>
        .matchup-table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
            color: #222;
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
        }
        .matchup-table th {
            background-color: #e9e9e9;
            padding: 10px;
            text-align: left;
            border: 1px solid #ddd;
            font-weight: bold;
        }
        .matchup-table td {
            padding: 8px;
            text-align: left;
            border: 1px solid #ddd;
        }
        .win-row {
            background-color: rgba(46, 204, 113, 0.1); /* Light green for wins */
        }
        .loss-row {
            background-color: rgba(255, 99, 71, 0.1); /* Light red for losses */
        }
        .matchup-table tr:hover {
            background-color: #f1f1f1;
        }
        .winner {
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    # Create the table rows dynamically
    rows = []
    for idx, row in matchup_df.iterrows():
        diff = row['User Score'] - row['Opponent Score']
        is_user_win = diff > 0
        
        if is_user_win:
            winner = username
            winner_score = row['User Score']
            loser_score = row['Opponent Score']
            row_class = 'win-row'
        else:
            winner = selected_manager_name
            winner_score = row['Opponent Score']
            loser_score = row['User Score']
            row_class = 'loss-row'
        
        # Prepare each row
        rows.append(f"""
            <tr class="{row_class}">
                <td>{idx + 1}</td>
                <td>{row['Season']}</td>
                <td>{row['Week']}</td>
                <td>{row['League']}</td>
                <td>{'**' if is_user_win else ''}{winner_score:.1f}{'**' if is_user_win else ''} - {'**' if not is_user_win else ''}{loser_score:.1f}{'**' if not is_user_win else ''}</td>
                <td class="winner">**{winner}**</td>
                <td>{abs(diff):.1f}</td>
            </tr>
        """)

    # Render the table
    st.markdown(f"""
        <table class="matchup-table">
            <thead>
                <tr>
                    <th>No.</th>
                    <th>Season</th>
                    <th>Week</th>
                    <th>League</th>
                    <th>Score</th>
                    <th>Winner</th>
                    <th>Diff</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>
    """, unsafe_allow_html=True)

