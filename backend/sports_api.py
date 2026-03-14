import os
import requests
from dotenv import load_dotenv
from datetime import date

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
        team_name = player["team"]["full_name"]
        return player["id"], full_name, team_name
    #player not found
    return None

#find team id, name
def find_team(name: str) -> tuple[int, str]:
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
        return "", ""
    
    player_id, full_name, team_name= player_stats
    #find player for this season
    stats_found = requests.get(f"{URL}/season_averages", headers=HEADERS_MAPPING, params={"player_ids[]": player_id, "season": 2025})
    #stats_found = requests.get(f"{URL}/season_averages", headers=HEADERS_MAPPING, params={"player_ids[]": player_id, "season": 2025})
    print(f"Status code: {stats_found.status_code}")
    print(f"Response: {stats_found.text}")

    averages= stats_found.json().get("data", [])
    if not averages:
        return "", team_name
    #return each statistical average for this season
    stats = averages[0]
    return(f"{full_name} stats: " f"{stats['pts']} PPG, " f"{stats['reb']} RPG, " f"{stats['ast']} APG, " f"{stats['fg_pct']*100:.1f}% FG, "f"{stats['fg3_pct']*100:.1f}% 3P, {stats['stl']} SPG, "
    f"{stats['blk']} BPG, {stats['turnover']} TOV\n"), team_name

def get_team_info(team_name:str) -> str:
    team_details = find_team(team_name)
    if team_details is None:
        return""
    #team name as details for now
    _, full_name = team_details
    return f"Team: {full_name}\n"


def get_matchup(team_name: str)-> str:
    matchup = find_team(team_name)
    if not matchup:
        return ""
    team_id, full_name = matchup
    matchup_tonight = date.today().isoformat()

    found = requests.get(f"{URL}/games",headers=HEADERS_MAPPING,params={"dates[]": matchup_tonight, "team_ids[]": team_id})
    matchups_found = found.json().get("data", [])

    if not matchups_found:
        return f"No game found for {full_name} tonight"
    
    game = matchups_found[0]
    home_team = game["home_team"]["full_name"]
    away_team = game["visitor_team"]["full_name"]
    return f"Tonights matchup: {away_team} vs {home_team}"

