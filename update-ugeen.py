import requests
import re

# بياناتك الخاصة (المستخرجة من تحليلك)
TOKEN = "eyDhbaciO:TU-JINSIsInR5cCIGIkpXVCJ9... (انسخ التوكن كاملاً هنا)"
BASE_API = "http://176.123.9.60:3000/v1"

def get_new_code():
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Accept': 'application/json'
    }
    try:
        # طلب الكود الجديد من السيرفر مباشرة
        response = requests.get(f"{BASE_API}/user/activation-code", headers=headers)
        data = response.json()
        # استخراج الكود (الرقم الطويل)
        return data.get('code') 
    except:
        return None

def update_playlist(new_code):
    if not new_code:
        print("❌ لم يتم الحصول على كود جديد")
        return

    # روابط القنوات مع الكود الجديد
    m3u_content = f"""#EXTM3U
#EXTINF:-1, beIN SPORTS 1 HD
http://ugeen.live:8080/live.php?id={new_code}&ch=beIN1
#EXTINF:-1, beIN SPORTS 2 HD
http://ugeen.live:8080/live.php?id={new_code}&ch=beIN2
#EXTINF:-1, SSC 1 HD
http://ugeen.live:8080/live.php?id={new_code}&ch=SSC1
"""
    
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print(f"✅ تم تحديث الملف بالكود الجديد: {new_code}")

if __name__ == "__main__":
    code = get_new_code()
    update_playlist(code)
