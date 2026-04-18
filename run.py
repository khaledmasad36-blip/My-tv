import requests

# التوكن النظيف الخاص بك
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjMyODUzNCwiaWF0IjoxNzc2NTE4NTg3LCJleHAiOjE3NzY2Njg1ODcsInR5cGUiOiJhY2Nlc3MiLCJ1c2VybmFtZSI6IkhnYmIiLCJlbWFpbCI6ImtoYWxlZG1hc2FkMzZAZ21haWwuY29tIiwicm9sZSI6InVzZXIiLCJzdGF0dXMiOjEsImlwdHYiOnsidXNlciI6IlVnZWVuX1ZJUHRhVDZaMyIsInBhc3MiOiJRZ1JRMWMifX0.t7O0qKwwHB3x5piQjoNbeB6zkfbEzYXN4f9y7fc4T14"

def start():
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    }
    try:
        # نجلب البيانات الصافية من السيرفر
        url = "http://176.123.9.60:3000/v1/users/me"
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            # استخراج البيانات المطلوبة للرابط الجديد
            iptv_user = data.get('iptv', {}).get('user')
            iptv_pass = data.get('iptv', {}).get('pass') # أضفنا الباسورد
            
            if iptv_user and iptv_pass:
                create_m3u(iptv_user, iptv_pass)
                print(f"✅ تم إنشاء الرابط بنجاح لليوزر: {iptv_user}")
            else:
                print("❌ لم نجد بيانات اليوزر أو الباسورد")
        else:
            print(f"❌ خطأ من السيرفر: {response.status_code}")
            
    except Exception as e:
        print(f"❌ فشل الاتصال: {e}")

def create_m3u(user, password):
    # هذه هي الصيغة الرسمية التي وجدناها في ملفاتك (get.php)
    # الهوست والبورت ثابتين حسب كود الموقع: http://ugeen.live:8080
    host = "http://ugeen.live:8080"
    
    final_link = f"{host}/get.php?username={user}&password={password}&type=m3u"
    
    # سنضع الرابط داخل ملف m3u ليتم قراءته من المشغلات
    content = f"#EXTM3U\n#EXTINF:-1, Ugeen IPTV Direct Link\n{final_link}"
    
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    start()
