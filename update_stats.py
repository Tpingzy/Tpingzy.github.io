import requests
import json
import datetime

API_KEY = "e110dcd6-cfe8-4714-a179-f517f3e364fc"
PLAYER_ID = 378 # Kristaps Porzingis

def update():
    now = datetime.datetime.now()
    # 改用生涯總數據 API 端點
    url = f"https://api.balldontlie.io/v1/players/{PLAYER_ID}/career_stats"
    headers = {"Authorization": API_KEY}
    
    try:
        print("🚀 正在抓取 KP 生涯總計數據...")
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code == 200:
            data = r.json()
            # 這裡直接取回傳的生涯數據
            stats = data.get('data', {})
            
            output = {
                "last_updated": now.strftime("%Y-%m-%d %H:%M:%S"),
                "is_career_total": True,
                "stats": stats
            }
            
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=4)
            print("✅ 生涯數據已存入 data.json")
        else:
            print(f"❌ API 錯誤: {r.status_code}")
    except Exception as e:
        print(f"❌ 發生錯誤: {e}")

if __name__ == "__main__":
    update()
