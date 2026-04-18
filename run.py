import requests

# التوكن الصافي اللي أرسلته
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjMyODUzNCwiaWF0IjoxNzc2NTE4NTg3LCJleHAiOjE3NzY2Njg1ODcsInR5cGUiOiJhY2Nlc3MiLCJ1c2VybmFtZSI6IkhnYmIiLCJlbWFpbCI6ImtoYWxlZG1hc2FkMzZAZ21haWwuY29tIiwicm9sZSI6InVzZXIiLCJzdGF0dXMiOjEsImlwdHYiOnsidXNlciI6IlVnZWVuX1ZJUHRhVDZaMyIsInBhc3MiOiJRZ1JRMWMifX0.t7O0qKwwHB3x5piQjoNbeB6zkfbEzYXN4f9y7fc4T14"

def start():
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    }
    try:
        # طلب البيانات من السيرفر
        url = "http://176.123.9.60:3000/v1/users/me"
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            # استخراج اليوزر من المكان الصحيح (iptv -> user)
            iptv_user = data.get('iptv', {}).get('user')
            
            if iptv_user:
                create_m3u(iptv_user)
                print(f"✅ تم سحب الكود بنجاح: {iptv_user}")
            else:
                write_to_file("# خطأ: لم نجد كلمة user داخل iptv")
        else:
            write_to_file(f"# خطأ من السيرفر رقم: {response.status_code}")
            
    except Exception as e:
        write_to_file(f"# فشل في الاتصال: {str(e)}")

def create_m3u(code):
    # الروابط باستخدام الكود المستخرج
    content = f"""#EXTM3U
#EXTINF:-1, beIN SPORTS 1 HD
http://ugeen.live:8080/live.php?id={code}&ch=beIN1
#EXTINF:-1, beIN SPORTS 2 HD
http://ugeen.live:8080/live.php?id={code}&ch=beIN2
#EXTINF:-1, SSC 1 HD
http://ugeen.live:8080/live.php?id={code}&ch=SSC1
"""
    write_to_file(content)

def write_to_file(text):
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(text)

if __name__ == "__main__":
    start()
