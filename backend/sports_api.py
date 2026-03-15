from nba_api.stats.endpoints import playercareerstats, scoreboardv2
from nba_api.stats.static import players, teams
from datetime import date

def find_player(name: str) -> dict | None:
    #Search for player
    players_list = players.find_players_by_full_name(name)
    if not players_list:
        players_list = players.find_players_by_last_name(name)
    if players_list:
        return players_list[0]
    return None

def get_player_stats(player_name: str) -> tuple[str, str]:
    #Fetch 2025-26 season averages for a player
    cur_player = find_player(player_name)
    if not cur_player:
        return "", ""

    try:
        career = playercareerstats.PlayerCareerStats(player_id=cur_player["id"])
        df = career.get_data_frames()[0]
        #print(f"Available seasons: {df['SEASON_ID'].tolist()}")

        # filter for 2025-26 season specifically
        season_df = df[df["SEASON_ID"] == "2025-26"]
        if season_df.empty:
            return "", ""

        latest = season_df.iloc[0]
        gp = latest["GP"]
        full_name = cur_player["full_name"]
        team_abbrev = latest["TEAM_ABBREVIATION"]
        # find team full name from abbreviation
        team_list = teams.find_team_by_abbreviation(team_abbrev)
        team_name = team_list["full_name"] if team_list else team_abbrev

        #grabs per game stats by dividing: total/gamesplayed
        stats_str = (
            f"{full_name} 2025-26 Averages: "
            f"{latest['PTS']/gp:.1f} PPG, "
            f"{latest['REB']/gp:.1f} RPG, "
            f"{latest['AST']/gp:.1f} APG, "
            f"{latest['FG_PCT']*100:.1f}% FG, "
            f"{latest['FG3_PCT']*100:.1f}% 3P, "
            f"{latest['STL']/gp:.1f} SPG, "
            f"{latest['BLK']/gp:.1f} BPG, "
            f"{latest['TOV']/gp:.1f} TOV\n"
        )
        return stats_str, team_name

    except Exception as e:
        print(f"Error fetching stats: {e}")
        import traceback
        traceback.print_exc()
        return "", ""

def get_team_info(team_name: str) -> str:
    #Fetch basic team info by name
    found = teams.find_teams_by_full_name(team_name)
    if not found:
        found = teams.find_teams_by_nickname(team_name)
    if found:
        return f"Team: {found[0]['full_name']}\n"
    return ""

def get_matchup(team_name: str) -> str:
    #Fetch tonight's game for a given team/player
    try:
        found = teams.find_teams_by_full_name(team_name)
        if not found:
            found = teams.find_teams_by_nickname(team_name)
        if not found:
            return ""

        team_id = found[0]["id"]
        today = date.today().strftime("%m/%d/%Y")

        scoreboard = scoreboardv2.ScoreboardV2(game_date=today)
        games_df = scoreboard.get_data_frames()[0]

        for _, game in games_df.iterrows():
            if game["HOME_TEAM_ID"] == team_id or game["VISITOR_TEAM_ID"] == team_id:
                home = teams.find_team_name_by_id(game["HOME_TEAM_ID"])
                away = teams.find_team_name_by_id(game["VISITOR_TEAM_ID"])
                return f"Tonight's matchup: {away} vs {home}\n"

        return f"No game found for {team_name} tonight.\n"

    except Exception as e:
        print(f"Error fetching matchup: {e}")
        return ""