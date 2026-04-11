import json
import time
import datetime
from nba_api.stats.endpoints import playercareerstats, playergamelog
from requests.exceptions import ReadTimeout

# Kristaps Porzingis NBA Player ID
PLAYER_ID = '204001'

custom_headers = {
    'Host': 'stats.nba.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://www.nba.com/' # 建議多加一個 Referer 增加真實性
}

def fetch_with_retry(endpoint_class, max_retries=3, **kwargs):
    """加入重試機制的 API 請求函式"""
    for attempt in range(max_retries):
        try:
            return endpoint_class(**kwargs)
        except ReadTimeout:
            print(f"⚠️ 連線逾時 (嘗試 {attempt + 1}/{max_retries})，等待 5 秒後重試...")
            time.sleep(5)
            if attempt == max_retries - 1:
                raise

def update_data():
    try:
        print("連線至 NBA 伺服器獲取生涯數據...")
        career = fetch_with_retry(
            playercareerstats.PlayerCareerStats, 
            player_id=PLAYER_ID, 
            headers=custom_headers, 
            timeout=30 # 縮短 timeout，提早觸發重試
        )
        career_df = career.get_data_frames()[0]
        career_totals = career.get_data_frames()[1]
        latest_season = career_df.iloc[-1]
        
        print("連線至 NBA 伺服器獲取最近比賽數據...")
        gamelog = fetch_with_retry(
            playergamelog.PlayerGameLog, 
            player_id=PLAYER_ID, 
            headers=custom_headers, 
            timeout=30
        )
        gamelog_df = gamelog.get_data_frames()[0]
        latest_game = gamelog_df.iloc[0]

        print("正在整理 Tingus Pingus 數據...")
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

        print("寫入 data.json...")
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)
            
        print("✅ 成功！")

    except Exception as e:
        print(f"❌ 發生錯誤: {e}")
        raise e

if __name__ == "__main__":
    update_data()
