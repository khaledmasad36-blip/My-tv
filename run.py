import requests

TOKEN = "ضـع_التـوكن_الخـاص_بـك_هنـا"

def start():
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Origin': 'http://ugeen.live',
        'Referer': 'http://ugeen.live/'
    }
    try:
        # الرابط المباشر للسيرفر
        response = requests.get("http://176.123.9.60:3000/v1/users/me", headers=headers, timeout=15)
        print(f"Server Status: {response.status_code}") # بيطبع لنا الرقم في الشاشة السوداء
        
        if response.status_code == 200:
            data = response.json()
            # استخراج الكود
            active_code = data.get('iptv', {}).get('username')
            if active_code:
                with open("playlist.m3u", "w", encoding="utf-8") as f:
                    f.write(f"#EXTM3U\n#EXTINF:-1, beIN 1\nhttp://ugeen.live:8080/live.php?id={active_code}&ch=beIN1")
                print(f"✅ Created with code: {active_code}")
            else:
                print("❌ Code not found in JSON response")
        else:
            print(f"❌ Error from server: {response.text}")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    start()
