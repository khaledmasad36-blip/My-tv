import requests
import re

def activate_ugeen_vips():
    # 1. محاولة جلب "التوكن" الشغال حالياً من مصدر خارجي نشط
    try:
        token_finder = requests.get("https://raw.githubusercontent.com/fomny/iptv/main/ugeen.m3u", timeout=10).text
        # استخراج التوكن (الذي يأتي بعد كلمة token=)
        match = re.search(r'token=([a-zA-Z0-9]+)', token_finder)
        token = match.group(1) if match else "ugeen2024"
    except:
        token = "ugeen2024" # توكن احتياطي

    # 2. قنواتك المفضلة (beIN و SSC و Alwan) من واقع ملفك اللي أرسلته
    # لاحظ أننا نستخدم "المعرفات" الخاصة بسيرفر يوجين
    channels = [
        {"name": "beIN SPORTS 1 HD", "id": "3019"},
        {"name": "beIN SPORTS 2 HD", "id": "3020"},
        {"name": "SSC 1 HD", "id": "1331"},
        {"name": "ALWAN Sports 1", "id": "4661"},
        {"name": "ALWAN Sports 2", "id": "4662"}
    ]
    
    # اسم المستخدم وكلمة السر من ملفك: Ugeen_VIPtaT6Z3 / QgRQ1c
    base_url = "http://ugeen.live:8080/live/Ugeen_VIPtaT6Z3/QgRQ1c/"
    
    final_m3u = "#EXTM3U\n"
    for ch in channels:
        # بناء الرابط الجديد مع التوكن
        link = f"{base_url}{ch['id']}.ts?token={token}"
        final_m3u += f"#EXTINF:-1, {ch['name']}\n{link}\n"
        
    # إضافة قنوات إضافية "مفتوحة" كاحتياط لضمان عدم فراغ القائمة
    try:
        extra = requests.get("https://raw.githubusercontent.com/Fazz-H/iptv/main/sports_arabic.m3u", timeout=5).text
        final_m3u += extra.replace("#EXTM3U", "")
    except:
        pass

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_m3u)
    print(f"تم التفعيل باستخدام التوكن: {token}")

if __name__ == "__main__":
    activate_ugeen_vips()
