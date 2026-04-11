import requests
import json
import datetime
import time

# 你的 API Key
API_KEY = "e110dcd6-cfe8-4714-a179-f517f3e364fc"
PLAYER_ID = 378 # KP 的 ID
START_YEAR = 2015 

def update():
    now = datetime.datetime.now()
    # 2026年4月應抓取 2025 賽季
    latest_season = now.year if now.month >= 10 else now.year - 1
    
    headers = {"Authorization": API_KEY}
    career_stats = []

    print(f"🚀 開始抓取 KP 生涯數據 (2015-{latest_season})...")

    for year in range(START_YEAR, latest_season + 1):
        # 修正 API 請求路徑格式
        url = "https://api.balldontlie.io/v1/season_averages"
        params = {
            "season": year,
            "player_ids[]": PLAYER_ID
        }
        
        try:
            r = requests.get(url, headers=headers, params=params, timeout=20)
            if r.status_code == 200:
                res_data = r.json()
                # 檢查 data 是否存在且有內容
                if res_data.get('data') and len(res_data['data']) > 0:
                    stat = res_data['data'][0]
                    stat['season_year'] = f"{year}-{str(year+1)[2:]}"
                    career_stats.append(stat)
                    print(f"✅ 獲取 {year} 成功")
                else:
                    print(f"⚠️ {year} 沒數據 (球員可能因傷缺賽或 API 未更新)")
            else:
                print(f"❌ API 報錯 {year}: {r.status_code}")
            
            # 免費版 API 有頻率限制，停 1.5 秒最穩陣
            time.sleep(1.5)
            
        except Exception as e:
            print(f"❌ {year} 出錯: {e}")

    # 寫入 data.json
    output = {
        "last_updated": now.strftime("%Y-%m-%d %H:%M:%S"),
        "stats": career_stats
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4, ensure_ascii=False)
    
    print(f"✨ 完成！共抓取到 {len(career_stats)} 季數據。")

if __name__ == "__main__":
    update()
