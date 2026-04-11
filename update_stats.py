import requests
import json
import datetime

API_KEY = "e110dcd6-cfe8-4714-a179-f517f3e364fc"
PLAYER_ID = 378  # Porzingis

def update():
    now = datetime.datetime.now()

    url = f"https://api.balldontlie.io/v1/season_averages?player_ids[]={PLAYER_ID}&season=2024"
    headers = {"Authorization": API_KEY}

    try:
        r = requests.get(url, headers=headers, timeout=20)
        data = r.json()

        stats = data.get("data", [])

        output = {
            "last_updated": now.strftime("%Y-%m-%d %H:%M:%S"),
            "stats": stats
        }

        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4)

        print("✅ 更新成功")

    except Exception as e:
        print(f"❌ 發生錯誤: {e}")

if __name__ == "__main__":
    update()
