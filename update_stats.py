import requests
import json
import datetime

API_KEY = "e110dcd6-cfe8-4714-a179-f517f3e364fc"
PLAYER_ID = 378 # Porzingis

def update():
    now = datetime.datetime.now()
    # 抓取生涯總計 API
    url = f"https://api.balldontlie.io/v1/players/{PLAYER_ID}/career_stats"
    headers = {"Authorization": API_KEY}
    
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code == 200:
            stats = r.json().get('data', {})
            output = {
                "last_updated": now.strftime("%Y-%m-%d %H:%M:%S"),
                "stats": stats # 這裡會是一個單一的數據物件
            }
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=4)
            print("✅ 生涯數據更新成功")
        else:
            print(f"❌ API 錯誤: {r.status_code}")
    except Exception as e:
        print(f"❌ 發生錯誤: {e}")

if __name__ == "__main__":
    update()
