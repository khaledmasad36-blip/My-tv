import requests

def get_elite_links():
    # روابط المطورين الذين يكسرون حماية beIN و SSC يومياً
    elite_sources = [
        "https://raw.githubusercontent.com/Mohamed-IPTV/free/main/sports.m3u",
        "https://raw.githubusercontent.com/Fazz-H/iptv/main/sports_arabic.m3u",
        "https://raw.githubusercontent.com/Mo3geza/Mo3geza/master/playlist.m3u"
    ]
    
    final_m3u = "#EXTM3U\n"
    added_urls = set()

    for url in elite_sources:
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                # تصفية القنوات لأخذ النخبة فقط (رياضة وألوان)
                lines = r.text.splitlines()
                for i in range(len(lines)):
                    if "#EXTINF" in lines[i] and any(k in lines[i].upper() for k in ["BEIN", "SSC", "ALWAN", "SPORT"]):
                        link = lines[i+1].strip()
                        if link not in added_urls:
                            final_m3u += lines[i] + "\n" + link + "\n"
                            added_urls.add(link)
        except:
            continue

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_m3u)
    print("تم جلب نخبة القنوات بنجاح!")

if __name__ == "__main__":
    get_elite_links()
