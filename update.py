import requests
import re

def ugeen_style_crawler():
    # هذه السيرفرات هي "المناجم" التي تسحب منها المواقع روابط beIN و Alwan
    # وهي سيرفرات Xtream مفتوحة (Public Panels)
    panels = [
        "http://pure-iptv.com:8080",
        "http://1.royal-iptv.top:8080",
        "http://line.hi-iptv.top:80"
    ]
    
    # حسابات تجريبية (غالباً ما تكون شغالة ويستخدمها الموزعون)
    user = "111"
    pw = "111"
    
    final_playlist = "#EXTM3U\n"
    target_channels = ["BEIN", "SSC", "ALWAN", "OSN"]
    
    for host in panels:
        try:
            # محاولة جلب قائمة القنوات مباشرة من السيرفر (مثلما يفعل يوجين)
            api_url = f"{host}/get.php?username={user}&password={pw}&type=m3u_plus&output=ts"
            print(f"محاولة سحب القنوات من: {host}")
            
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200 and "#EXTM3U" in response.text:
                lines = response.text.splitlines()
                for i in range(len(lines)):
                    if lines[i].startswith("#EXTINF"):
                        # إذا وجدنا قناة رياضية أو ألوان
                        if any(key in lines[i].upper() for key in target_keywords):
                            final_playlist += lines[i] + "\n" + lines[i+1] + "\n"
                print(f"نجح السحب من {host}!")
                break # إذا وجدنا سيرفر شغال نتوقف
        except:
            continue

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_playlist)

if __name__ == "__main__":
    ugeen_style_crawler()
