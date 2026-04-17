import requests

def get_ugeen_links():
    # هذه هي الروابط التي يستخدمها موقع يوجين عادةً لتغذية تطبيقاته
    ugeen_sources = [
        "https://ugeen.live/playlist.m3u",
        "https://ugeen.live/iptv.m3u",
        "https://ugeen.live/free.m3u"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36",
        "Referer": "https://ugeen.live/"
    }
    
    final_data = "#EXTM3U\n"
    
    for url in ugeen_sources:
        try:
            # نحاول الدخول كأننا "تطبيق جوال" وليس كمبيوتر
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200 and "#EXTINF" in response.text:
                final_data += response.text.replace("#EXTM3U", "")
                print(f"تم بنجاح سحب المصدر: {url}")
        except:
            continue

    if len(final_data) > 10:
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(final_data)
    else:
        print("موقع يوجين يغلق الوصول المباشر حالياً، جاري جلب البديل الرياضي الأقوى...")
        # هنا نضع المصدر الرياضي المضمون كبديل في حال فشل يوجين
        fallback = requests.get("https://raw.githubusercontent.com/Fazz-H/iptv/main/sports_arabic.m3u")
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(fallback.text)

if __name__ == "__main__":
    get_ugeen_links()
