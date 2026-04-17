import requests

def update_sports_channels():
    # روابط مباشرة ومجربة لقنوات beIN و SSC والرياضية السعودية
    # هذه المصادر تعتبر "المناجم" الأساسية لأغلب تطبيقات الـ IPTV
    urls = [
        "https://raw.githubusercontent.com/Fazz-H/iptv/main/sports_arabic.m3u",
        "https://raw.githubusercontent.com/m3uplaylist/arab/main/sports.m3u"
    ]
    
    combined_data = "#EXTM3U\n"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    for url in urls:
        try:
            r = requests.get(url, headers=headers, timeout=20)
            if r.status_code == 200:
                # نأخذ محتوى الملف ونزيل سطر البداية المتكرر
                content = r.text.replace("#EXTM3U", "")
                combined_data += content + "\n"
        except:
            continue

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(combined_data)
    print("تم تحديث قنوات beIN و SSC بنجاح!")

if __name__ == "__main__":
    update_sports_channels()
