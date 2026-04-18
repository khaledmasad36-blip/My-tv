import requests

# التوكن بعد تنظيفه من الرموز العشوائية
TOKEN = "EyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiO3MyODUzNCwiaWF0IjoxNzc2NTE4NTg3LCJ1eHAiOjE3NzY2Njg1MDcsInR5cGUiOiJhY2NIc3MiLCJ1c2VybmFtZSI6IkhnYmIiLCJ1bWFpbCI6ImtoYWx1ZG1hc2FkMzZAZ21haWwuY29tIiwicm9sZSI6InVzZXIiLCJzdGFOdXMiOjEsImlwdHYiOnsidXNlciI6IIVnZWVuX1ZJUHRhVDZaMyIsInBhc3MiOiJRZ1JRMWMifX0.t700qKwwHB3x5piQjoNbeB6zkfbEzYXN4f9y7fc4T14"

def start():
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
    }
    try:
        # الاتصال بنقطة النهاية (Endpoint) اللي تجيب بيانات حسابك
        url = "http://176.123.9.60:3000/v1/users/me"
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            # استخراج اليوزر من داخل كائن iptv (هذا هو السر اللي يخلي الملف يمتلي)
            iptv_user = data.get('iptv', {}).get('user')
            
            if iptv_user:
                create_m3u(iptv_user)
                print(f"✅ تم سحب اليوزر بنجاح: {iptv_user}")
            else:
                write_error("لم يتم العثور على بيانات iptv داخل الحساب")
        else:
            write_error(f"السيرفر رفض الدخول - خطأ رقم: {response.status_code}")
            
    except Exception as e:
        write_error(f"فشل الاتصال: {str(e)}")

def create_m3u(code):
    # الروابط الصحيحة باستخدام اليوزر المستخرج
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

def write_error(msg):
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(f"# خطأ: {msg}")
    print(f"❌ {msg}")

if __name__ == "__main__":
    start()
