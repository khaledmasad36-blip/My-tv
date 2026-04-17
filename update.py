import requests
import re

def get_hybrid_streams():
    # مصادر مبرمجين عرب يقومون بتحديث توكن يوجين وألوان يدوياً كل ساعة
    # هذه الروابط هي "خلاصة" ما يتم تفعيله في المجموعات الخاصة
    special_sources = [
        "https://raw.githubusercontent.com/Mohamed-IPTV/free/main/ugeen_sports.m3u",
        "https://raw.githubusercontent.com/fomny/iptv/main/main.m3u",
        "https://raw.githubusercontent.com/Fazz-H/iptv/main/sports_arabic.m3u"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    final_m3u = "#EXTM3U\n"
    # كلمات البحث عن القنوات التي تهمك
    target_channels = ["UGEEN", "ALWAN", "BEIN", "SSC", "SPORTS"]
    
    unique_links = set()

    for url in special_sources:
        try:
            print(f"جاري فحص المصدر: {url}")
            r = requests.get(url, headers=headers, timeout=15)
            if r.status_code == 200:
                lines = r.text.splitlines()
                for i in range(len(lines)):
                    if lines[i].startswith("#EXTINF"):
                        # التأكد أن القناة رياضية أو تابعة ليوجين/ألوان
                        if any(key in lines[i].upper() for key in target_channels):
                            link = lines[i+1].strip()
                            if link not in unique_links:
                                final_m3u += lines[i] + "\n" + link + "\n"
                                unique_links.add(link)
        except:
            continue

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_m3u)
    print(f"تم بنجاح تجهيز {len(unique_links)} قناة.")

if __name__ == "__main__":
    get_hybrid_streams()
