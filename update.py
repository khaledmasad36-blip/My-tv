import requests

def manual_fix():
    # روابطك الـ VIP مع توكن محدث
    # ملاحظة: إذا توقفت القنوات، فقط سنغير التوكن في هذا السطر
    token = "ugeen24" 
    
    content = "#EXTM3U\n"
    channels = [
        {"name": "beIN SPORTS 1 VIP", "url": "http://premium.ugeen.live:80/live/ugeen/ugeen/beIN_SPORTS_1_EN.m3u8"},
        {"name": "SSC 1 VIP", "url": "http://premium.ugeen.live:80/live/ugeen/ugeen/SSC_1_HD.m3u8"},
        {"name": "SSC 2 VIP", "url": "http://premium.ugeen.live:80/live/ugeen/ugeen/SSC_2_HD.m3u8"},
        {"name": "SSC EXTRA 1", "url": "http://premium.ugeen.live:80/live/ugeen/ugeen/SSC_EXTRA_1_HD.m3u8"}
    ]
    
    for ch in channels:
        content += f"#EXTINF:-1, {ch['name']}\n{ch['url']}?token={token}\n"
    
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(content)
    print("تم تثبيت روابط VIP!")

if __name__ == "__main__":
    manual_fix()
