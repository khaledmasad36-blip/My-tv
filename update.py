import requests

def update_to_direct_streams():
    # مصادر روابط مباشرة وقوية جداً (تحدث تلقائياً من المطورين)
    sources = [
        "https://raw.githubusercontent.com/Fazz-H/iptv/main/sports_arabic.m3u",
        "https://raw.githubusercontent.com/Mohamed-IPTV/free/main/sports.m3u"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    final_m3u = "#EXTM3U\n"
    
    for url in sources:
        try:
            print(f"جاري جلب البث من: {url}")
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                # نأخذ محتوى الملف وننظفه
                clean_data = response.text.replace("#EXTM3U", "")
                final_m3u += clean_data + "\n"
        except:
            continue

    # حفظ الملف
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_m3u)
    print("تم تحديث القنوات بروابط مباشرة!")

if __name__ == "__main__":
    update_to_direct_streams()
