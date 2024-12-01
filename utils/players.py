# utils/players.py
import json
import os
from datetime import datetime, timedelta
import requests

CACHE_FILE = "utils/players_cache.json"
CACHE_DURATION = timedelta(days=1)

class PlayerCache:
    @staticmethod
    def get_players():
        if not os.path.exists(CACHE_FILE):
            return PlayerCache._update_cache()
        
        file_time = datetime.fromtimestamp(os.path.getmtime(CACHE_FILE))
        if datetime.now() - file_time > CACHE_DURATION:
            return PlayerCache._update_cache()
        
        try:
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading cache: {e}")
            return PlayerCache._update_cache()

    @staticmethod
    def _update_cache():
        try:
            response = requests.get("https://api.sleeper.app/v1/players/nfl")
            if response.status_code == 200:
                players = response.json()
                os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
                with open(CACHE_FILE, 'w') as f:
                    json.dump(players, f)
                return players
        except Exception as e:
            print(f"Error updating cache: {e}")
            return {}

player_cache = PlayerCache()