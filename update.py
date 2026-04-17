import requests
import re

def bypass_and_fetch():
    # روابط "خزانات" الروابط المفعلة (هذه يتم تحديثها من مبرمجين تخطوا الكود يدوياً)
    bypass_sources = [
        "https://raw.githubusercontent.com/Mohamed-IPTV/free/main/ugeen_sports.m3u",
        "https://raw.githubusercontent.com/fomny/iptv/main/ugeen.m3u",
        "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ar.m3u" # مصدر احتياطي عالمي
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "*/*"
    }
    
    final_playlist = "#EXTM3U\n"
    seen_urls = set() # لمنع تكرار القنوات

    for url in bypass_sources:
        try:
            print(f"محاولة جلب الروابط من: {url}")
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                lines = response.text.splitlines()
                for i in range(len(lines)):
                    # نبحث عن السطر الذي يحتوي على اسم القناة (beIN أو SSC)
                    if lines[i].startswith("#EXTINF") and ("BEIN" in lines[i].upper() or "SSC" in lines[i].upper()):
                        channel_url = lines[i+1]
                        if channel_url not in seen_urls:
                            final_playlist += lines[i] + "\n" + channel_url + "\n"
                            seen_urls.add(channel_url)
        except Exception as e:
            print(f"فشل في الوصول لـ {url}: {e}")
            continue

    # حفظ الملف النهائي
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_playlist)
    print(f"تم بنجاح جمع {len(seen_urls)} قناة رياضية مفعلة.")

if __name__ == "__main__":
    bypass_and_fetch()
