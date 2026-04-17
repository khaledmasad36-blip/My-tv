import requests

def update_sports_playlist():
    # مصادر متخصصة في القنوات الرياضية العربية والعالمية
    sources = [
        "https://raw.githubusercontent.com/m3uplaylist/arab/main/sports.m3u",
        "https://raw.githubusercontent.com/shantnu/Arabic-IPTV/master/channels/sports.m3u",
        "https://iptv-org.github.io/iptv/categories/sports.m3u"
    ]
    
    combined_content = "#EXTM3U\n"
    
    for url in sources:
        try:
            # وضعنا مهلة زمنية 10 ثوانٍ لكل مصدر
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                lines = response.text.splitlines()
                # نتأكد أن الملف يحتوي على بيانات فعلاً
                if len(lines) > 1:
                    # ندمج المحتوى مع حذف سطر البداية المتكرر
                    combined_content += "\n".join([line for line in lines if not line.startswith("#EXTM3U")]) + "\n"
                print(f"تم جلب قنوات رياضية من: {url}")
        except:
            print(f"المصدر {url} غير متاح حالياً")

    # حفظ الملف النهائي في مشروعك
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(combined_content)
    print("سيرفر الرياضة جاهز!")

if __name__ == "__main__":
    update_sports_playlist()
