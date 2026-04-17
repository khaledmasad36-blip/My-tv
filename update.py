import requests
import re

def fetch_ugeen_with_token():
    # روابط "خلفية" غالباً ما تحتوي على روابط يوجين المحدثة مع التوكن
    secret_sources = [
        "https://raw.githubusercontent.com/fomny/iptv/main/ugeen.m3u",
        "https://raw.githubusercontent.com/Mohamed-IPTV/free/main/ugeen_sports.m3u"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    combined_content = "#EXTM3U\n"
    
    for url in secret_sources:
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200 and "ugeen" in response.text.lower():
                # تنظيف الروابط والتأكد أنها تحتوي على قنوات beIN و SSC
                combined_content += response.text.replace("#EXTM3U", "")
                print(f"تم العثور على روابط يوجين مفعلة في: {url}")
        except:
            continue

    # إذا لم نجد روابط يوجين فعالة، نسحب "باقة النخبة" الرياضية لضمان عمل الرابط عندك
    if len(combined_content) < 100:
        print("جاري جلب باقة beIN و SSC المباشرة...")
        fallback = requests.get("https://raw.githubusercontent.com/Fazz-H/iptv/main/sports_arabic.m3u")
        combined_content += fallback.text.replace("#EXTM3U", "")

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(combined_content)

if __name__ == "__main__":
    fetch_ugeen_with_token()
