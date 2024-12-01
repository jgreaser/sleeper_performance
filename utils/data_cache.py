# utils/data_cache.py
import streamlit as st
from typing import Dict, List, Optional
from functools import lru_cache
import pandas as pd
from utils.api import (
    get_user_id,
    get_user_leagues,
    get_league_data,
    get_users,
    get_rosters,
    get_matchups_for_week,
    get_playoff_bracket
)

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_cached_league_info(league_id: str):
    """Cache league info to minimize API calls"""
    league_data = get_league_data(league_id)
    users = get_users(league_id)
    rosters = get_rosters(league_id)
    playoff_bracket = get_playoff_bracket(league_id)
    
    return {
        'league_data': league_data,
        'users': users,
        'rosters': rosters,
        'playoff_bracket': playoff_bracket
    }

@st.cache_data(ttl=3600)
def get_cached_matchups(league_id: str, week: int):
    """Cache matchup data to minimize API calls"""
    return get_matchups_for_week(league_id, week)

@st.cache_data(ttl=3600)
def get_cached_user_leagues(user_id: str, season: Optional[str] = None):
    """Cache user leagues to minimize API calls"""
    return get_user_leagues(user_id, season)

def get_user_performance_optimized(username: str):
    """Optimized version of get_user_performance"""
    user_id = get_user_id(username)
    if not user_id:
        return None
    
    performance_data = []
    cached_league_data = {}
    
    # Get all leagues first
    for season in range(2015, 2025):
        leagues = get_cached_user_leagues(user_id, str(season))
        if not leagues:
            continue
            
        # Batch fetch league data
        for league in leagues:
            league_id = league['league_id']
            cached_league_data[league_id] = get_cached_league_info(league_id)
    
    # Process the cached data
    for season in range(2015, 2025):
        leagues = get_cached_user_leagues(user_id, str(season))
        if leagues:
            for league in leagues:
                try:
                    league_id = league['league_id']
                    league_info = cached_league_data.get(league_id)
                    
                    if not league_info:
                        continue
                        
                    rosters = league_info['rosters']
                    league_data = league_info['league_data']
                    
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
                        
                        total_teams = len(rosters)
                        
                        # Check if user is champion
                        is_champion = False
                        if (league_data and 
                            isinstance(league_data, dict) and 
                            league_data.get('status') == 'complete' and 
                            isinstance(league_data.get('metadata'), dict)):
                            winner_roster_id = league_data.get('metadata', {}).get('latest_league_winner_roster_id')
                            if winner_roster_id:
                                is_champion = str(user_roster['roster_id']) == str(winner_roster_id)
                        
                        # Calculate achievements - exactly matching the expected column names
                        performance_data.append({
                            'Season': season,
                            'League': league['name'],
                            'Games Above 500': wins - losses,
                            'Standing': standing,
                            'Total Teams': total_teams,
                            'Is Regular Season Winner': standing == 1,
                            'Is Champion': is_champion,  # Now matches exactly
                            'In Top 6': standing <= 6 if total_teams >= 8 else standing <= (total_teams * 0.75),
                            'In Bottom 4': standing > (total_teams - 4) if total_teams >= 8 else standing > (total_teams * 0.5),
                            'league_id': league_id
                        })
                except Exception as e:
                    st.warning(f"Error processing league for season {season}: {str(e)}")
                    continue
    
    # Create DataFrame and ensure all boolean columns are properly typed
    df = pd.DataFrame(performance_data)
    boolean_columns = ['Is Champion', 'Is Regular Season Winner', 'In Top 6', 'In Bottom 4']
    for col in boolean_columns:
        df[col] = df[col].astype(bool)
    
    return df

def analyze_head_to_head_optimized(league_ids: List[str], user_id: str, opponent_id: str):
    """Optimized version of analyze_head_to_head including playoff matchups"""
    matchup_history = []
    
    for league_id in league_ids:
        league_info = get_cached_league_info(league_id)
        if not league_info:
            continue
            
        league_data = league_info['league_data']
        rosters = league_info['rosters']
        playoff_bracket = league_info['playoff_bracket']
        
        if not league_data or not rosters:
            continue
        
        # Create user ID to roster ID mapping
        user_to_roster = {
            roster['owner_id']: roster['roster_id']
            for roster in rosters
            if roster.get('owner_id')
        }
        
        user_roster_id = user_to_roster.get(user_id)
        opponent_roster_id = user_to_roster.get(opponent_id)
        
        if not user_roster_id or not opponent_roster_id:
            continue
            
        season = league_data['season']
        reg_season_weeks = league_data.get('settings', {}).get('playoff_week_start', 14)
        
        # Regular Season Matchups
        for week in range(1, reg_season_weeks):
            matchups = get_cached_matchups(league_id, week)
            if not matchups:
                continue
            
            user_matchup = next((m for m in matchups if m['roster_id'] == user_roster_id), None)
            opponent_matchup = next((m for m in matchups if m['roster_id'] == opponent_roster_id), None)
            
            if (user_matchup and opponent_matchup and 
                user_matchup.get('matchup_id') == opponent_matchup.get('matchup_id')):
                
                user_score = float(user_matchup.get('points', 0))
                opp_score = float(opponent_matchup.get('points', 0))
                
                if user_score == 0 and opp_score == 0:
                    continue

                matchup_history.append({
                    'Season': int(season),
                    'Week': week,
                    'League': league_data['name'],
                    'User Score': round(user_score, 2),
                    'Opponent Score': round(opp_score, 2),
                    'Result': 'Win' if user_score > opp_score else 'Loss' if user_score < opp_score else 'Tie',
                    'Type': 'Regular Season'
                })
        
        # Playoff Matchups
        if playoff_bracket:
            # Find direct matchups in the playoff bracket
            playoff_matchup = next(
                (match for match in playoff_bracket 
                 if (match.get('t1') == user_roster_id and match.get('t2') == opponent_roster_id) or
                    (match.get('t1') == opponent_roster_id and match.get('t2') == user_roster_id)),
                None
            )
            
            if playoff_matchup:
                round_num = playoff_matchup.get('r')
                week = reg_season_weeks + round_num - 1
                
                round_names = {
                    1: "First Round",
                    2: "Semi-Finals",
                    3: "Finals"
                }
                playoff_round = round_names.get(round_num, f"Round {round_num}")
                
                matchups = get_cached_matchups(league_id, week)
                if matchups:
                    user_matchup = next((m for m in matchups if m['roster_id'] == user_roster_id), None)
                    opponent_matchup = next((m for m in matchups if m['roster_id'] == opponent_roster_id), None)
                    
                    if user_matchup and opponent_matchup:
                        user_score = float(user_matchup.get('points', 0))
                        opp_score = float(opponent_matchup.get('points', 0))
                        
                        if user_score == 0 and opp_score == 0:
                            continue
                        
                        matchup_history.append({
                            'Season': int(season),
                            'Week': playoff_round,
                            'League': league_data['name'],
                            'User Score': round(user_score, 2),
                            'Opponent Score': round(opp_score, 2),
                            'Result': 'Win' if user_score > opp_score else 'Loss' if user_score < opp_score else 'Tie',
                            'Type': 'Playoffs'
                        })
    
    df = pd.DataFrame(matchup_history)
    if not df.empty:
        df = df.sort_values(['Season', 'Week'], ascending=[False, True])
    return df