import json
from nba_api.stats.endpoints import playercareerstats, playergamelog
import datetime

# Kristaps Porzingis NBA Player ID
PLAYER_ID = '204001'

def update_data():
    # 1. Get Career & Season Stats
    career = playercareerstats.PlayerCareerStats(player_id=PLAYER_ID)
    career_df = career.get_data_frames()[0]
    career_totals = career.get_data_frames()[1] # API provides total averages

    # Get latest season row
    latest_season = career_df.iloc[-1]
    
    # 2. Get Recent Game
    # Assuming current season is 2023-24 (Update if needed, or omit season to get default current)
    gamelog = playergamelog.PlayerGameLog(player_id=PLAYER_ID)
    gamelog_df = gamelog.get_data_frames()[0]
    latest_game = gamelog_df.iloc[0]

    # 3. Format Data
    data = {
        "last_updated": str(datetime.datetime.now()),
        "recent_game": {
            "date": latest_game['GAME_DATE'],
            "matchup": latest_game['MATCHUP'],
            "pts": int(latest_game['PTS']),
            "reb": int(latest_game['REB']),
            "blk": int(latest_game['BLK'])
        },
        "season": {
            "season_year": latest_season['SEASON_ID'],
            "pts": round(latest_season['PTS'] / latest_season['GP'], 1),
            "reb": round(latest_season['REB'] / latest_season['GP'], 1),
            "blk": round(latest_season['BLK'] / latest_season['GP'], 1),
            "fg3_pct": round(latest_season['FG3_PCT'] * 100, 1)
        },
        "career": {
            "games_played": int(career_totals['GP'].iloc[0]),
            "pts_avg": round(career_totals['PTS'].iloc[0] / career_totals['GP'].iloc[0], 1),
            "reb_avg": round(career_totals['REB'].iloc[0] / career_totals['GP'].iloc[0], 1),
            "blk_avg": round(career_totals['BLK'].iloc[0] / career_totals['GP'].iloc[0], 1),
            "total_pts": int(career_totals['PTS'].iloc[0])
        }
    }

    # 4. Save to JSON
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    update_data()
