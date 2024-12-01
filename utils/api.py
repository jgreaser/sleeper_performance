import requests

def get_user_id(username):
    """Get user ID from username"""
    response = requests.get(f"https://api.sleeper.app/v1/user/{username}")
    if response.status_code == 200:
        user_data = response.json()
        if user_data and 'user_id' in user_data:  # Check if user_data exists and has user_id
            return user_data['user_id']
    return None

def get_user_leagues(user_id, season=None):
    """
    Get leagues for a user for a specific season or all seasons.
    Args:
        user_id: The numerical ID of the user
        season: Optional season year (e.g., '2023', '2024'). If None, gets current season.
    """
    if not user_id:  # Add check for user_id
        return None
        
    if season:
        response = requests.get(f"https://api.sleeper.app/v1/user/{user_id}/leagues/nfl/{season}")
    else:
        response = requests.get(f"https://api.sleeper.app/v1/user/{user_id}/leagues/nfl")
    
    if response.status_code == 200:
        leagues = response.json()
        return leagues if leagues else None
    return None

def get_league_data(league_id):
    """Get detailed information about a specific league"""
    response = requests.get(f"https://api.sleeper.app/v1/league/{league_id}")
    return response.json() if response.status_code == 200 else None

def get_users(league_id):
    response = requests.get(f"https://api.sleeper.app/v1/league/{league_id}/users")
    return response.json() if response.status_code == 200 else None

def get_rosters(league_id):
    response = requests.get(f"https://api.sleeper.app/v1/league/{league_id}/rosters")
    return response.json() if response.status_code == 200 else None

def get_players():
    response = requests.get("https://api.sleeper.app/v1/players/nfl")
    return response.json() if response.status_code == 200 else None

def get_player_stats(season_type, season, week):
    response = requests.get(f"https://api.sleeper.app/v1/stats/nfl/{season}/{season_type}/{week}")
    return response.json() if response.status_code == 200 else None

def get_weekly_matchups(league_id, week):
    response = requests.get(f"https://api.sleeper.app/v1/league/{league_id}/matchups/{week}")
    return response.json() if response.status_code == 200 else None

def get_playoff_bracket(league_id):
    """Get playoff bracket information for a league"""
    response = requests.get(f"https://api.sleeper.app/v1/league/{league_id}/winners_bracket")
    return response.json() if response.status_code == 200 else None

def get_league_winner(league_id):
    """Get the winner of a league by checking league metadata"""
    # Get league data
    league_data = get_league_data(league_id)
    
    if league_data and 'metadata' in league_data:
        # Check if there's a winner roster ID in metadata
        winner_roster_id = league_data['metadata'].get('latest_league_winner_roster_id')
        
        if winner_roster_id:
            # Get rosters to match the winner roster ID to owner
            rosters = get_rosters(league_id)
            if rosters:
                winner_roster = next(
                    (r for r in rosters if str(r['roster_id']) == str(winner_roster_id)), 
                    None
                )
                if winner_roster:
                    return winner_roster.get('owner_id')
    
    return None

def get_matchups_for_week(league_id, week):
    """Get matchup data for a specific week"""
    response = requests.get(f"https://api.sleeper.app/v1/league/{league_id}/matchups/{week}")
    return response.json() if response.status_code == 200 else None