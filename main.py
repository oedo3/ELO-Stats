from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import pandas as pd

# Step 1: Search for player
player_dict = players.find_players_by_full_name("Lebron James")
player_id = player_dict[0]['id']

# Step 2: Fetch career stats
career = playercareerstats.PlayerCareerStats(player_id=player_id)
df = career.get_data_frames()[0]  # Full career summary

# Step 3: Show data
print(df[['SEASON_ID', 'TEAM_ID', 'PTS', 'AST', 'REB', 'FG_PCT', 'FG3_PCT', 'FT_PCT']])
