import requests

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjMyODUzNCwiaWF0IjoxNzc2NTE4NTg3LCJleHAiOjE3NzY2Njg1ODcsInR5cGUiOiJhY2Nlc3MiLCJ1c2VybmFtZSI6IkhnYmIiLCJlbWFpbCI6ImtoYWxlZG1hc2FkMzZAZ21haWwuY29tIiwicm9sZSI6InVzZXIiLCJzdGF0dXMiOjEsImlwdHYiOnsidXNlciI6IlVnZWVuX1ZJUHRhVDZaMyIsInBhc3MiOiJRZ1JRMWMifX0.t7O0qKwwHB3x5piQjoNbeB6zkfbEzYXN4f9y7fc4T14"

def start():
    # إضافة معلومات متصفح حقيقي (User-Agent) و Referer لتمويه السيرفر
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'http://ugeen.live',
        'Referer': 'http://ugeen.live/',
        'Accept-Language': 'ar-SA,ar;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    try:
        url = "http://176.123.9.60:3000/v1/users/me"
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            iptv_user = data.get('iptv', {}).get('user')
            if iptv_user:
                create_m3u(iptv_user)
                print(f"✅ Success! User: {iptv_user}")
            else:
                write_to_file("# Error: Data found but no iptv user")
        elif response.status_code == 403:
            # إذا استمر الـ 403، بنستخدم اليوزر اللي استخرجناه يدوياً من التوكن كحل احتياطي
            print("⚠️ 403 detected. Using backup info from token.")
            create_m3u("Ugeen_VIPtaV6Z3")
        else:
            write_to_file(f"# Server Error: {response.status_code}")
            
    except Exception as e:
        write_to_file(f"# Connection Failed: {str(e)}")

def create_m3u(code):
    content = f"""#EXTM3U
#EXTINF:-1, beIN SPORTS 1 HD
http://ugeen.live:8080/live.php?id={code}&ch=beIN1
#EXTINF:-1, beIN SPORTS 2 HD
http://ugeen.live:8080/live.php?id={code}&ch=beIN2
#EXTINF:-1, SSC 1 HD
http://ugeen.live:8080/live.php?id={code}&ch=SSC1
"""
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(content)

def write_to_file(text):
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(text)

if __name__ == "__main__":
    start()
