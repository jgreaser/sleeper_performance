import streamlit as st
from utils.api import (
    get_user_id,
    get_user_leagues,
    get_league_data,
    get_users,
    get_rosters,
)


# Username input section
st.header("This is QUITE the broken page, don't bother")
username = st.text_input("Enter your Sleeper username:", key="username_input")

if username:
    # First get the user ID
    user_id = get_user_id(username)
    
    if user_id:
        # Get available seasons (2017 onwards)
        available_seasons = list(range(2024, 2016, -1))
        selected_season = st.selectbox(
            "Select Season:",
            available_seasons,
            index=0
        )
        
        # Get leagues for selected season
        leagues = get_user_leagues(user_id, str(selected_season))
        
        if leagues:
            # Create league selection dropdown
            league_options = {
                f"{league['name']} ({league['season']})": league 
                for league in leagues
            }
            
            selected_league_name = st.selectbox(
                "Select your league:",
                options=list(league_options.keys()),
                key="league_selector"
            )
            
            if selected_league_name:
                league = league_options[selected_league_name]
                league_id = league['league_id']
                
                # Display league information
                col1, col2 = st.columns(2)
                
                with col1:
                    st.header("League Information")
                    st.write(f"League Name: {league['name']}")
                    st.write(f"Season: {league['season']}")
                    st.write(f"Status: {league['status']}")
                
                # Fetch league data
                users = get_users(league_id)
                rosters = get_rosters(league_id)
                
                if users and rosters:
                    # Create users dataframe
                    users_df = pd.DataFrame([{
                        'Display Name': user['display_name'],
                        'Team Name': user.get('metadata', {}).get('team_name', 'N/A'),
                        'Points': next((roster['settings']['fpts'] 
                                   for roster in rosters 
                                   if roster['owner_id'] == user['user_id']), 0),
                        'Wins': next((roster['settings']['wins']
                                    for roster in rosters
                                    if roster['owner_id'] == user['user_id']), 0),
                        'Losses': next((roster['settings']['losses']
                                      for roster in rosters
                                      if roster['owner_id'] == user['user_id']), 0)
                    } for user in users])
                    
                    with col2:
                        st.header("League Standings")
                        st.dataframe(
                            users_df[['Display Name', 'Team Name', 'Points', 'Wins', 'Losses']]
                            .sort_values('Points', ascending=False),
                            hide_index=True
                        )
                else:
                    st.error("Unable to fetch league data. Please try again.")
        else:
            st.error(f"No leagues found for this user in {selected_season} season.")
    else:
        st.error("Username not found. Please check the username and try again.")
