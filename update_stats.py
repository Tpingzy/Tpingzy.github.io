import requests
import json
import datetime
import time

# 你的 API Key
API_KEY = "e110dcd6-cfe8-4714-a179-f517f3e364fc"
PLAYER_ID = 378
START_YEAR = 2015  # KP 入行年份

def update_career_stats():
    # 自動獲取今年年份 (2026)
    current_year = datetime.datetime.now().year
    # 如果現在是 4 月，球季還在 2025-26 (即 API 的 2025 賽季)
    # 如果是 10 月後，則可能開始抓 2026 賽季
    latest_season = current_year if datetime.datetime.now().month >= 10 else current_year - 1
    
    url = "https://api.balldontlie.io/v1/season_averages"
    headers = {"Authorization": API_KEY}
    
    all_career_data = []

    print(f"🚀 開始抓取 Tingus Pingus 生涯數據 ({START_YEAR} - {latest_season})...")

    for year in range(START_YEAR, latest_season + 1):
        # 2016 年 KP 因為受傷或特殊情況可能沒數據，API 會回傳空值，我們要處理
        params = {
            "season": year,
            "player_ids[]": PLAYER_ID
        }
        
        try:
            response = requests.get(url, params=params, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data.get('data'):
                    stats = data['data'][0]
                    # 加入年份標記方便辨識
                    stats['display_season'] = f"{year}-{str(year+1)[2:]}"
                    all_career_data.append(stats)
                    print(f"✅ 已獲取 {year} 賽季")
                else:
                    print(f"ℹ️ {year} 賽季無數據 (可能因傷缺賽)")
            
            # 免費版 API 限制每分鐘請求次數，加個微小延遲保險
            time.sleep(0.2) 
            
        except Exception as e:
            print(f"❌ 抓取 {year} 出錯: {e}")

    # 存檔
    output = {
        "last_updated": str(datetime.datetime.now()),
        "player_id": PLAYER_ID,
        "career_stats": all_career_data
    }

    with open('kp_career_full.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4, ensure_ascii=False)
    
    print(f"\n✨ 全部完成！總共儲存了 {len(all_career_data)} 個賽季的數據到 kp_career_full.json")

if __name__ == "__main__":
    update_career_stats()
