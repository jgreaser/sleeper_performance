import pandas as pd
from .api import get_rosters, get_league_winner

def process_league_data(user_id, leagues_data):
    """Process league data to include championship information"""
    league_results = []
    
    for league in leagues_data:
        league_id = league['league_id']
        user_roster = None
        rosters = get_rosters(league_id)
        
        if rosters:
            user_roster = next((r for r in rosters if r['owner_id'] == user_id), None)
        
        if user_roster:
            winner_id = get_league_winner(league_id)
            is_champion = winner_id == user_id if winner_id else False
            
            league_results.append({
                'Season': league['season'],
                'League': league['name'],
                'Total Teams': len(rosters),
                'Standing': user_roster['settings']['rank'],
                'Points': user_roster['settings'].get('fpts', 0),
                'Is Champion': is_champion,
                # ... other fields ...
            })
    
    return pd.DataFrame(league_results)
    
def create_users_df(users, rosters):
    return pd.DataFrame([{
        'Display Name': user['display_name'],
        'Team Name': user.get('metadata', {}).get('team_name', 'N/A'),
        'Points': next((roster['settings']['fpts'] 
                       for roster in rosters 
                       if roster['owner_id'] == user['user_id']), 0),
        'user_id': user['user_id']
    } for user in users])

def create_roster_df(roster, players_data, weekly_stats):
    if not roster or not players_data:
        return pd.DataFrame()
        
    player_list = []
    for player_id in roster['players']:
        player = players_data.get(player_id, {})
        season_stats = aggregate_player_stats(player_id, weekly_stats)
        
        player_list.append({
            'Name': f"{player.get('first_name', '')} {player.get('last_name', '')}",
            'Position': player.get('position', 'N/A'),
            'Team': player.get('team', 'N/A'),
            'Season Points': round(season_stats['pts_ppr'], 1),
            'Total TDs': season_stats['td'],
            'Pass Yards': season_stats['pass_yd'],
            'Rush Yards': season_stats['rush_yd'],
            'Rec Yards': season_stats['rec_yd'],
            'player_id': player_id
        })
    return pd.DataFrame(player_list)

def aggregate_player_stats(player_id: str, weekly_matchups: dict) -> dict:
    total_stats = {
        'pts_ppr': 0,
        'td': 0,
        'pass_yd': 0,
        'rush_yd': 0,
        'rec_yd': 0,
        'weekly_points': []
    }
    
    for week, matchups in weekly_matchups.items():
        for matchup in matchups:
            if player_id in matchup.get('players_points', {}):
                points = matchup['players_points'].get(player_id, 0)
                total_stats['pts_ppr'] += points
                total_stats['weekly_points'].append(points)
            else:
                total_stats['weekly_points'].append(0)

    return total_stats