import requests

# التوكن حقك (تأكد إنه لسه فعال)
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjMyODUzNCwiaWF0IjoxNzc2NTE4NTg3LCJleHAiOjE3NzY2Njg1ODcsInR5cGUiOiJhY2Nlc3MiLCJ1c2VybmFtZSI6IkhnYmIiLCJlbWFpbCI6ImtoYWxlZG1hc2FkMzZAZ21haWwuY29tIiwicm9sZSI6InVzZXIiLCJzdGF0dXMiOjEsImlwdHYiOnsidXNlciI6IlVnZWVuX1ZJUHRhVDZaMyIsInBhc3MiOiJRZ1JRMWMifX0.t7O0qKwwHB3x5piQjoNbeB6zkfbEzYXN4f9y7fc4T14"

def start():
    # الهيدرز هنا هي السر، خليتها تطابق المتصفح تماماً
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ar,en-US;q=0.7,en;q=0.3',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    # بياناتك اللي سحبناها
    user = "Ugeen_VIPtaV6Z3"
    password = "QgRQM1c"
    host = "http://ugeen.live:8080"
    
    # الرابط اللي لقيته أنت في ملف generator
    target_url = f"{host}/get.php?username={user}&password={password}&type=m3u"
    
    try:
        # بنحاول نحمل محتوى الملف الفعلي
        response = requests.get(target_url, headers=headers, timeout=20)
        
        if response.status_code == 200 and "#EXTM3U" in response.text:
            # لو السيرفر أعطانا ملف M3U حقيقي، بننسخه زي ما هو
            with open("playlist.m3u", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("✅ تم سحب القنوات بنجاح!")
        else:
            # لو فشل في سحب الملف، بنسوي روابط "يدوية" لكن بصيغة متطورة
            create_manual_m3u(host, user, password)
            print("⚠️ السيرفر رفض التحميل المباشر، تم إنشاء روابط يدوية احتياطية.")
            
    except Exception as e:
        create_manual_m3u(host, user, password)
        print(f"❌ خطأ: {e}")

def create_manual_m3u(host, user, password):
    # صيغة الـ MPEG-TS (أكثر صيغة مستقرة في السيرفرات المجانية)
    content = f"""#EXTM3U
#EXTINF:-1, beIN SPORTS 1 HD
{host}/{user}/{password}/1
#EXTINF:-1, beIN SPORTS 2 HD
{host}/{user}/{password}/2
#EXTINF:-1, SSC 1 HD
{host}/{user}/{password}/3
"""
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    start()
