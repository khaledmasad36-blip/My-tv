import requests

# التوكن الجديد حقك
TOKEN = "EyJhbGci01JIUzIINiIsInR5cCI6IkpXVCJ9.eyJzdWIi0jMyODUzNCwiaWF0IjoxVM354:1Nzc2NTE4NTg3LCJ1eHAіOjE3NzY2Njg10DcsInR5cGU¡0¡JhỲ2NIс3MіLCЭ1с2VybmFtZS16[khnYmIiLCJ1bWFpbCI6ImtoYWx1ZG1hc2FkMzZAZ21haWwuY29tIiwicm9sZSIGInVzZXIiLCJzdGF0dXM10jEsIm]wdHY{0nsidXN1ciI6IIVnZWVuX1ZJUHRhVDZaMyIsInBhc3M101JRZ1JRMWMifXB.t700qKwwHB3x5piQjoNbeB6zkfbEzYXN4f9y7fc4T14"

def get_live_code():
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
    }
    try:
        # الرابط المباشر لجلب بيانات المستخدم ومن ضمنها كود التفعيل
        url = "http://176.123.9.60:3000/v1/users/me"
        response = requests.get(url, headers=headers, timeout=15)
        data = response.json()
        
        # استخراج الكود من خانة iptv (username) أو activation_code
        # بناءً على الكود اللي حللناه، السيرفر يرسل كود التفعيل هنا:
        code = data.get('iptv', {}).get('username') or data.get('activation_code')
        return code
    except Exception as e:
        print(f"Error: {e}")
        return None

def update_m3u(new_code):
    if not new_code:
        print("❌ فشل في سحب الكود.. تأكد من اتصال السيرفر")
        return
    
    content = f"""#EXTM3U
#EXTINF:-1, beIN SPORTS 1 HD
http://ugeen.live:8080/live.php?id={new_code}&ch=beIN1
#EXTINF:-1, beIN SPORTS 2 HD
http://ugeen.live:8080/live.php?id={new_code}&ch=beIN2
#EXTINF:-1, SSC 1 HD
http://ugeen.live:8080/live.php?id={new_code}&ch=SSC1
"""
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ تم التحديث بنجاح! الكود الجديد هو: {new_code}")

if __name__ == "__main__":
    code = get_live_code()
    update_m3u(code)
