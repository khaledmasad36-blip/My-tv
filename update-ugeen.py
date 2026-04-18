import requests
import re

# التوكن حقك (المفتاح الطويل ey...)
TOKEN = "ضـع_التـوكن_الخـاص_بـك_هنـا"

def get_live_code():
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'User-Agent': 'Mozilla/5.0'
    }
    try:
        # السيرفر اللي شفناه في الكود حقك
        url = "http://176.123.9.60:3000/v1/users/me" 
        response = requests.get(url, headers=headers)
        # هنا السيرفر بيرسل بياناتك ومن ضمنها كود التفعيل النشط حالياً
        data = response.json()
        
        # بنحاول نسحب الكود من خانة 'activationCode' أو أي خانة تشبهها
        # ملاحظة: إذا كان السيرفر يرسل الكود في ملف نصي، بنعدل الرابط
        return data.get('activation_code') or data.get('code')
    except Exception as e:
        print(f"Error fetching code: {e}")
        return None

def update_m3u(new_code):
    if not new_code:
        print("❌ فشل في الحصول على الكود الجديد.. تأكد من التوكن")
        return
    
    # النص اللي بيظهر في التلفزيون
    content = f"""#EXTM3U
#EXTINF:-1, beIN SPORTS 1 HD
http://ugeen.live:8080/live.php?id={new_code}&ch=beIN1
#EXTINF:-1, beIN SPORTS 2 HD
http://ugeen.live:8080/live.php?id={new_code}&ch=beIN2
#EXTINF:-1, SSC 1 HD
http://ugeen.live:8080/live.php?id={new_code}&ch=SSC1"""

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ تم التحديث بالكود الجديد: {new_code}")

if __name__ == "__main__":
    current_code = get_live_code()
    update_m3u(current_code)
