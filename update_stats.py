import requests
import json
import datetime
import time

# 確保呢度嘅 Key 同 ID 係正確嘅
API_KEY = "e110dcd6-cfe8-4714-a179-f517f3e364fc"
PLAYER_ID = 378 # KP 的 ID
START_YEAR = 2015 

def update():
    now = datetime.datetime.now()
    current_year = now.year
    latest_season = current_year if now.month >= 10 else current_year - 1
    
    headers = {"Authorization": API_KEY}
    career_stats = []

    print(f"🚀 嘗試抓取 2015-{latest_season} 數據...")

    for year in range(START_YEAR, latest_season + 1):
        # 使用正確的 balldontlie API 格式
        url = f"https://api.balldontlie.io/v1/season_averages?season={year}&player_ids[]={PLAYER_ID}"
        try:
            r = requests.get(url, headers=headers, timeout=20)
            if r.status_code == 200:
                data = r.json()
                if data.get('data') and len(data['data']) > 0:
                    stat = data['data'][0]
                    stat['season_year'] = f"{year}-{str(year+1)[2:]}"
                    career_stats.append(stat)
                    print(f"✅ 成功獲取 {year}")
                else:
                    print(f"⚠️ {year} 沒數據 (可能受傷缺賽)")
            else:
                print(f"❌ API 報錯 {year}: {r.status_code}")
            time.sleep(1) # 增加延遲，確保唔會被 API Block
        except Exception as e:
            print(f"❌ {year} 發生錯誤: {e}")

    # 寫入檔案
    output = {
        "last_updated": str(now),
        "stats": career_stats
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4)
    
    if len(career_stats) > 0:
        print(f"✨ 成功！總共抓到 {len(career_stats)} 季數據。")
    else:
        print("🛑 警告：最終列表依然係空嘅，請檢查 API Key 是否有效。")

if __name__ == "__main__":
    update()
