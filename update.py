import requests

def final_fix_alwan_sports():
    # مصادر بديلة قوية جداً لقنوات ألوان و beIN و SSC (تحدث كل ساعة)
    sources = [
        "https://raw.githubusercontent.com/Fazz-H/iptv/main/sports_arabic.m3u",
        "https://raw.githubusercontent.com/Mohamed-IPTV/free/main/sports.m3u",
        "https://raw.githubusercontent.com/fomny/iptv/main/main.m3u"
    ]
    
    headers = {"User-Agent": "Mozilla/5.0"}
    final_m3u = "#EXTM3U\n"
    
    # الكلمات التي نبحث عنها لضمان وجود القنوات التي طلبتها
    target_keywords = ["ALWAN", "BEIN", "SSC", "SPORTS"]
    seen_urls = set()

    for url in sources:
        try:
            r = requests.get(url, headers=headers, timeout=15)
            if r.status_code == 200:
                lines = r.text.splitlines()
                for i in range(len(lines)):
                    if lines[i].startswith("#EXTINF"):
                        # فحص القناة بالاسم
                        name_line = lines[i].upper()
                        if any(key in name_line for key in target_keywords):
                            link = lines[i+1].strip()
                            if link not in seen_urls and link.startswith("http"):
                                final_m3u += lines[i] + "\n" + link + "\n"
                                seen_urls.add(link)
        except:
            continue

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_m3u)
    print(f"تم بنجاح جلب {len(seen_urls)} قناة رياضية!")

if __name__ == "__main__":
    final_fix_alwan_sports()
