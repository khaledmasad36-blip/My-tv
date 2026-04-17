import requests

def get_pro_sports():
    # هذه المصادر هي الأقوى حالياً لقنوات beIN و SSC و Alwan Sports
    sources = [
        "https://raw.githubusercontent.com/Fazz-H/iptv/main/sports_arabic.m3u",
        "https://raw.githubusercontent.com/Mohamed-IPTV/free/main/sports.m3u"
    ]
    
    headers = {"User-Agent": "Mozilla/5.0"}
    final_m3u = "#EXTM3U\n"
    
    # الكلمات التي تهمك فقط
    keywords = ["BEIN", "SSC", "ALWAN", "AL KASS", "AD SPORTS"]
    
    seen_urls = set()

    for url in sources:
        try:
            r = requests.get(url, headers=headers, timeout=15)
            if r.status_code == 200:
                lines = r.text.splitlines()
                for i in range(len(lines)):
                    if lines[i].startswith("#EXTINF"):
                        # فحص إذا كانت القناة رياضية من التي طلبتها
                        if any(key in lines[i].upper() for key in keywords):
                            link = lines[i+1].strip()
                            if link not in seen_urls:
                                # سنقوم بتنظيم الاسم ليظهر بشكل جميل في التلفزيون
                                final_m3u += lines[i] + "\n" + link + "\n"
                                seen_urls.add(link)
        except:
            continue

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_m3u)
    print(f"تم بنجاح جلب {len(seen_urls)} قناة رياضية مختارة!")

if __name__ == "__main__":
    get_pro_sports()
