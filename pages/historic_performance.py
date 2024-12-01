#test
import streamlit as st
import pandas as pd
from utils.api import (
    get_user_id,
    get_user_leagues,
    get_league_data,
    get_users,
    get_rosters,
    get_matchups_for_week
)
from components.performance_chart import display_performance_chart, display_comparison_chart
from components.head_to_head import display_head_to_head_summary
from components.matchup_table import display_matchup_table
from components.career_summary import format_stat, display_career_summary
from utils.data_cache import (
    get_user_performance_optimized,
    analyze_head_to_head_optimized
)

def get_user_performance(username):
    """Get performance data for a user"""
    user_id = get_user_id(username)
    if not user_id:
        return None
    
    performance_data = []
    
    for season in range(2015, 2025):
        leagues = get_user_leagues(user_id, str(season))
        if leagues:
            for league in leagues:
                try:  # Add try/except block for better error handling
                    league_id = league['league_id']
                    rosters = get_rosters(league_id)
                    users = get_users(league_id)
                    league_data = get_league_data(league_id)
                    
                    # Skip this league if we don't have all required data
                    if not all([rosters, users, league_data]):
                        continue
                    
                    user_roster = next((r for r in rosters if r['owner_id'] == user_id), None)
                    if user_roster:
                        wins = user_roster['settings'].get('wins', 0)
                        losses = user_roster['settings'].get('losses', 0)
                        
                        # Sort rosters by wins to get standing
                        sorted_rosters = sorted(rosters, 
                                             key=lambda x: (x['settings'].get('wins', 0), 
                                                          x['settings'].get('fpts', 0)), 
                                             reverse=True)
                        standing = next((i + 1 for i, r in enumerate(sorted_rosters) 
                                      if r['roster_id'] == user_roster['roster_id']), None)
                        
                        # Check if user is champion - only for completed seasons
                        is_champion = False
                        # More defensive championship check
                        try:
                            if (league_data and 
                                isinstance(league_data, dict) and 
                                league_data.get('status') == 'complete' and 
                                isinstance(league_data.get('metadata'), dict)):
                                winner_roster_id = league_data.get('metadata', {}).get('latest_league_winner_roster_id')
                                if winner_roster_id:
                                    is_champion = str(user_roster['roster_id']) == str(winner_roster_id)
                        except:
                            is_champion = False
                        
                        # Calculate various achievements
                        total_teams = len(rosters)
                        is_regular_season_winner = standing == 1
                        is_last = standing == total_teams
                        in_top_6 = standing <= 6 if total_teams >= 8 else standing <= (total_teams * 0.75)
                        in_bottom_4 = standing > (total_teams - 4) if total_teams >= 8 else standing > (total_teams * 0.5)
                        
                        performance_data.append({
                            'Season': season,
                            'League': league['name'],
                            'Games Above 500': wins - losses,
                            'Standing': standing,
                            'Total Teams': total_teams,
                            'Is Regular Season Winner': is_regular_season_winner,
                            'Is Last': is_last,
                            'In Top 6': in_top_6,
                            'In Bottom 4': in_bottom_4,
                            'Is Champion': is_champion,
                            'league_id': league_id
                        })
                except Exception as e:
                    st.warning(f"Error processing league for season {season}: {str(e)}")
                    continue
    
    return pd.DataFrame(performance_data)

def display_debug_info(debug_data, username, opponent_name):
    """Display debug information for playoff detection"""
    st.markdown("### Debug Information - Playoff Detection")
    st.markdown(f"Analyzing matchups between **{username}** and **{opponent_name}**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Leagues", debug_data['total_leagues_checked'])
    with col2:
        st.metric("Leagues with Playoffs", debug_data['leagues_with_playoffs'])
    with col3:
        st.metric("Playoff Matchups Found", len(debug_data['playoff_matchups_found']))
    
    if debug_data['playoff_matchups_found']:
        st.markdown("#### Found Playoff Matchups:")
        for match in debug_data['playoff_matchups_found']:
            st.markdown(f"""
            - Season: {match['season']}
              - League: {match['league']}
              - Round: {match['round']}
            """)
    else:
        st.warning("No playoff matchups were found between these users")

def analyze_head_to_head(league_ids, user_id, opponent_id, username, opponent_name):
    """Analyze head-to-head matchups between two users"""
    matchup_history = []
    debug_info = {
        'total_leagues_checked': len(league_ids),
        'leagues_with_playoffs': 0,
        'playoff_brackets_found': [],
        'playoff_matchups_found': []
    }
    
    # Place debug info display before processing matchups
    st.markdown("---")  # Add separator
    display_debug_info(debug_info, username, opponent_name)
    st.markdown("---")  # Add separator

def get_manager_mapping(league_ids):
    """Get mapping of user_ids to their most recent display names"""
    manager_data = {}
    
    for league_id in league_ids:
        users = get_users(league_id)
        league_data = get_league_data(league_id)
        if users and league_data:
            season = int(league_data.get('season', '0'))
            for user in users:
                user_id = user.get('user_id')
                if user_id:
                    if user_id not in manager_data or season > manager_data[user_id]['season']:
                        manager_data[user_id] = {
                            'display_name': user.get('display_name', 'Unknown'),
                            'season': season
                        }
    
    return {uid: data['display_name'] for uid, data in manager_data.items()}

# Main app
st.title("Historic Performance Analysis")

username = st.text_input("Enter your Sleeper username:")

if username:
    #performance_df = get_user_performance(username)
    performance_df = get_user_performance_optimized(username)


    if performance_df is not None and not performance_df.empty:
        # Display career summary first

        filter_container = st.container()
        
        with filter_container:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                min_year = int(performance_df['Season'].min())
                max_year = int(performance_df['Season'].max())
                year_range = st.slider(
                    "Select Year Range",
                    min_value=min_year,
                    max_value=max_year,
                    value=(min_year, max_year)
                )
            
            filtered_by_year = performance_df[
                (performance_df['Season'] >= year_range[0]) & 
                (performance_df['Season'] <= year_range[1])
            ]
            
            with col2:
                league_selections = st.multiselect(
                    "Select leagues to include:",
                    options=filtered_by_year['League'].unique(),
                    default=filtered_by_year['League'].unique()
                )
            
            # Filter data based on both year range and league selection
            filtered_df = performance_df[
                (performance_df['Season'] >= year_range[0]) & 
                (performance_df['Season'] <= year_range[1]) &
                (performance_df['League'].isin(league_selections))
            ]
            display_career_summary(filtered_df)
            
            # Get managers only from selected leagues
            if not filtered_df.empty:
                unique_league_ids = filtered_df['league_id'].unique()
                manager_mapping = get_manager_mapping(unique_league_ids)
                
                # Remove the current user from the manager options
                user_id = get_user_id(username)
                if user_id:
                    manager_mapping.pop(user_id, None)
                
                with col3:
                    selected_manager_name = st.selectbox(
                        "Compare with another manager:",
                        options=sorted(manager_mapping.values()),
                        key='manager_selector'
                    )

        # Display performance chart after the career summary
        display_performance_chart(filtered_df, username)

        # If a manager is selected for comparison
        if selected_manager_name:
            selected_manager_id = next(
                (uid for uid, name in manager_mapping.items() if name == selected_manager_name),
                None
            )
            
            if selected_manager_id:
                # Display comparison chart first
                compare_df = get_user_performance(selected_manager_name)
                if compare_df is not None and not compare_df.empty:
                    compare_filtered = compare_df[
                        (compare_df['Season'] >= year_range[0]) & 
                        (compare_df['Season'] <= year_range[1]) &
                        (compare_df['League'].isin(league_selections))
                    ]
                    
                    if not compare_filtered.empty:
                        display_comparison_chart(filtered_df, compare_filtered, 
                                              username, selected_manager_name)

                # Then display head-to-head analysis
                h2h_df = analyze_head_to_head_optimized(
                    filtered_df['league_id'].unique(),
                    user_id,
                    selected_manager_id
                )
                
                if not h2h_df.empty:
                    display_head_to_head_summary(username, selected_manager_name, h2h_df)
                    #display_matchup_table(h2h_df, username, selected_manager_name)
                else:
                    st.warning(f"No head-to-head matchups found with {selected_manager_name}")
    else:
        st.error("No leagues found for this username or the username doesn't exist.")