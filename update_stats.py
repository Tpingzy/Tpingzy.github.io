import requests
import json
import datetime
import time

API_KEY = "e110dcd6-cfe8-4714-a179-f517f3e364fc"
PLAYER_ID = 378 
START_YEAR = 2015 

def update():
    now = datetime.datetime.now()
    # 自動判定最新賽季 (2026年4月會抓 2025 賽季)
    latest_season = now.year if now.month >= 10 else now.year - 1
    
    headers = {"Authorization": API_KEY}
    career_stats = []

    print(f"🚀 抓取 2015-{latest_season} 數據...")

    for year in range(START_YEAR, latest_season + 1):
        url = f"https://api.balldontlie.io/v1/season_averages?season={year}&player_ids[]={PLAYER_ID}"
        try:
            r = requests.get(url, headers=headers, timeout=15)
            if r.status_code == 200:
                data = r.json()
                if data.get('data'):
                    stat = data['data'][0]
                    stat['season_year'] = f"{year}-{str(year+1)[2:]}"
                    career_stats.append(stat)
            time.sleep(0.5) 
        except Exception as e:
            print(f"Error in {year}: {e}")

    # 寫入 data.json
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump({"last_updated": str(now), "stats": career_stats}, f, indent=4)
    print("✅ Done!")

if __name__ == "__main__":
    update()
