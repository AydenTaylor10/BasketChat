import os
import requests
from dotenv import load_dotenv

load_dotenv()

BALLDONTLIE_API_KEY = os.getenv("BALLDONTLIE_API_KEY")
URL = "https://api.balldontlie.io/v1"
HEADERS_MAPPING = {"Authorization": BALLDONTLIE_API_KEY}

#find player id name
def find_player(name: str) -> tuple[int, str]:
    found = requests.get(f"{URL}/players",headers=HEADERS_MAPPING,params={"search": name})
    results_found = found.json().get("data", [])
    
    if results_found:
        #add player to results
        player = results_found[0]
        full_name = f"{player['first_name']} {player['last_name']}"
        return player["id"], full_name
    #player not found
    return None

#find team id, name
def find_team(name: str) -> tupe[int, str]:
    found = requests.get(f"{URL}/teams",headers=HEADERS_MAPPING,params={"search": name})
    team_results_found = found.json().get("data", [])

    if team_results_found:
        #add team to results
        team = team_results_found[0]
        return team["id"], team["full_name"]
    
    #team not found
    return None

def get_player_stats(player_name: str) -> str:
    player_stats = find_player(player_name)
    if player_stats is None:
        return ""
    
    player_id, full_name = player_stats
    #find player for this season
    stats_found = requests.get(f"{URL}/season_averages", headers=HEADERS_MAPPING, params={"player_ids[]": player_id, "season": 2025})
    