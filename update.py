import requests

def update_top_sports():
    # مصادر مخصصة لاصطياد قنوات beIN و SSC و AD
    sources = [
        "https://raw.githubusercontent.com/ybeghdadi/iptv/master/beinsports.m3u",
        "https://raw.githubusercontent.com/Fazz-H/iptv/main/sports_arabic.m3u",
        "https://raw.githubusercontent.com/Helios-13/IPTV/main/Arab/Sports.m3u"
    ]
    
    combined_content = "#EXTM3U\n"
    
    for url in sources:
        try:
            # نضع معلومات متصفح حقيقي لتجنب الحظر
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                lines = response.text.splitlines()
                if len(lines) > 1:
                    # نجمع فقط القنوات الرياضية ونستبعد أي شيء آخر
                    combined_content += "\n".join([line for line in lines if not line.startswith("#EXTM3U")]) + "\n"
        except:
            continue

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(combined_content)
    print("تم تحديث باقة beIN و SSC بنجاح!")

if __name__ == "__main__":
    update_top_sports()
