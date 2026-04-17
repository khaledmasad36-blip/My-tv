import requests
import re

def update_premium_sports():
    # أقوى مصادر حالية تحتوي على الباقات الرياضية المشفرة
    sources = [
        "https://raw.githubusercontent.com/MoXmo/IPTV/main/Arab.m3u",
        "https://raw.githubusercontent.com/Fazz-H/iptv/main/sports_arabic.m3u"
    ]
    
    final_playlist = "#EXTM3U\n"
    # الكلمات المفتاحية للقنوات التي تريدها
    targets = ["BEIN", "SSC", "SAUDI SPORT", "AD SPORT"]
    
    headers = {"User-Agent": "Mozilla/5.0"}
    
    for url in sources:
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                lines = response.text.splitlines()
                for i in range(len(lines)):
                    # إذا وجدنا سطر الوصف (اللي فيه اسم القناة)
                    if lines[i].startswith("#EXTINF"):
                        # نتحقق هل اسم القناة يحتوي على الكلمات التي نريدها؟
                        if any(target in lines[i].upper() for target in targets):
                            # نضيف سطر الوصف وسطر الرابط الذي يليه مباشرة
                            final_playlist += lines[i] + "\n" + lines[i+1] + "\n"
        except:
            continue

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_playlist)
    print("تم تجهيز باقة SSC و beIN بنجاح!")

if __name__ == "__main__":
    update_premium_sports()
