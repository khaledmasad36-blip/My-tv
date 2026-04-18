import requests

# هذا التوكن حقك بعد التنظيف
TOKEN = "EyJhbGci01JIUzIINiIsInR5cCI6IkpXVCJ9.eyJzdWIi0jMyODUzNCwiaWF0IjoxVM354-1Nzc2NTE4NTg3LCJ1eHAіOjE3NzY2Njg10DcsInR5cGU¡0¡JhỲ2NIс3MіLCЭ1с2VybmFtZS16khnYmIiLCJ1bWFpbCI6ImtoYWx1ZG1hc2FkMzZAZ21haWwuY29tIiwicm9sZSIGInVzZXIiLCJzdGF0dXM10jEsImwdHY0nsidXN1ciI6IIVnZWVuX1ZJUHRhVDZaMyIsInBhc3M101JRZ1JRMWMifXB.t700qKwwHB3x5piQjoNbeB6zkfbEzYXN4f9y7fc4T14"

def start():
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'User-Agent': 'Mozilla/5.0'
    }
    try:
        response = requests.get("http://176.123.9.60:3000/v1/users/me", headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # استخراج الكود
            active_code = data.get('iptv', {}).get('username') or "NoCodeFound"
            create_m3u(active_code)
            print(f"✅ Success! Code: {active_code}")
        else:
            print(f"❌ Error {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def create_m3u(code):
    content = f"#EXTM3U\n#EXTINF:-1, beIN 1\nhttp://ugeen.live:8080/live.php?id={code}&ch=beIN1"
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    start()
