import requests

def final_solution():
    # مصادر "خام" ومباشرة لا تطلب كود تفعيل (أقوى الموجود حالياً)
    sources = [
        "https://raw.githubusercontent.com/Fazz-H/iptv/main/sports_arabic.m3u",
        "https://raw.githubusercontent.com/Mohamed-IPTV/free/main/sports.m3u",
        "https://iptv-org.github.io/iptv/languages/ara.m3u"
    ]
    
    headers = {"User-Agent": "Mozilla/5.0"}
    final_content = "#EXTM3U\n"
    
    for url in sources:
        try:
            r = requests.get(url, headers=headers, timeout=15)
            if r.status_code == 200:
                # نأخذ القنوات ونضيفها (مع استبعاد سطر البداية المتكرر)
                data = r.text.replace("#EXTM3U", "")
                final_content += data + "\n"
        except:
            continue

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_content)
    print("تم تحديث القنوات بنجاح من المصادر البديلة!")

if __name__ == "__main__":
    final_solution()
