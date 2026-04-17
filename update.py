import requests

def create_playlist():
    # روابط مباشرة ومجربة لقنوات beIN و SSC وألوان
    # يتم سحبها من سيرفرات ثابتة لا تحتاج تفعيل يوجين
    channels = [
        {"name": "beIN SPORTS 1 HD", "url": "https://mohamed-iptv.top/live/beIN_1.m3u8"},
        {"name": "beIN SPORTS 2 HD", "url": "https://mohamed-iptv.top/live/beIN_2.m3u8"},
        {"name": "SSC 1 HD", "url": "https://mohamed-iptv.top/live/SSC_1.m3u8"},
        {"name": "SSC 2 HD", "url": "https://mohamed-iptv.top/live/SSC_2.m3u8"},
        {"name": "ALWAN Sports 1", "url": "http://cdn.alwan-sports.com:8080/live/alwan1/playlist.m3u8"},
        {"name": "ALWAN Sports 2", "url": "http://cdn.alwan-sports.com:8080/live/alwan2/playlist.m3u8"}
    ]
    
    content = "#EXTM3U\n"
    for ch in channels:
        content += f"#EXTINF:-1, {ch['name']}\n{ch['url']}\n"
        
    # محاولة إضافة قنوات إضافية من مصدر خارجي موثوق
    try:
        r = requests.get("https://raw.githubusercontent.com/Fazz-H/iptv/main/sports_arabic.m3u", timeout=10)
        if r.status_code == 200:
            content += r.text.replace("#EXTM3U", "")
    except:
        pass

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(content)
    print("تم إنشاء قائمة القنوات بنجاح!")

if __name__ == "__main__":
    create_playlist()
