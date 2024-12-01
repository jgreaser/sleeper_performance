import pandas as pd

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