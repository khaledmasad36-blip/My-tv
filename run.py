import requests

# التوكن الصافي حقك
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjMyODUzNCwiaWF0IjoxNzc2NTE4NTg3LCJleHAiOjE3NzY2Njg1ODcsInR5cGUiOiJhY2Nlc3MiLCJ1c2VybmFtZSI6IkhnYmIiLCJlbWFpbCI6ImtoYWxlZG1hc2FkMzZAZ21haWwuY29tIiwicm9sZSI6InVzZXIiLCJzdGF0dXMiOjEsImlwdHYiOnsidXNlciI6IlVnZWVuX1ZJUHRhVDZaMyIsInBhc3MiOiJRZ1JRMWMifX0.t7O0qKwwHB3x5piQjoNbeB6zkfbEzYXN4f9y7fc4T14"

def start():
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    }
    
    # بياناتك الاحتياطية (اللي طلعناها من التوكن) عشان نضمن ظهور الروابط
    backup_user = "Ugeen_VIPtaV6Z3"
    backup_pass = "QgRQM1c"
    
    try:
        url = "http://176.123.9.60:3000/v1/users/me"
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            iptv = data.get('iptv', {})
            user = iptv.get('user') or iptv.get('username') or backup_user
            password = iptv.get('pass') or backup_pass
            
            create_m3u(user, password)
            print(f"✅ Done! Created with User: {user}")
        else:
            # لو السيرفر أعطى خطأ، لا يوقف، يستخدم الاحتياطي
            create_m3u(backup_user, backup_pass)
            print("⚠️ Server error, used backup data.")
            
    except Exception as e:
        # حتى لو فشل الاتصال تماماً، بيسوي الملف بالبيانات الاحتياطية
        create_m3u(backup_user, backup_pass)
        print(f"✅ Emergency backup used due to error: {e}")

def create_m3u(user, password):
    host = "http://ugeen.live:8080"
    # الروابط بصيغة Xtream Codes اللي يطلبها السيرفر الحين
    content = f"""#EXTM3U
#EXTINF:-1, beIN SPORTS 1 HD
{host}/live/{user}/{password}/beIN1.m3u8
#EXTINF:-1, beIN SPORTS 2 HD
{host}/live/{user}/{password}/beIN2.m3u8
#EXTINF:-1, SSC 1 HD
{host}/live/{user}/{password}/SSC1.m3u8
#EXTINF:-1, FULL M3U LIST (Download)
{host}/get.php?username={user}&password={password}&type=m3u
"""
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    start()
