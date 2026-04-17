import requests
import re

def update_ugeen_vip():
    # 1. المصدر الذي سنجلب منه "التوكن" الجديد والشغال
    token_source = "https://raw.githubusercontent.com/fomny/iptv/main/ugeen.m3u"
    
    try:
        # جلب التوكن الجديد
        response = requests.get(token_source, timeout=15)
        # البحث عن التوكن داخل روابط المصدر (غالباً يكون بعد كلمة token=)
        match = re.search(r'token=([a-zA-Z0-9]+)', response.text)
        
        if match:
            new_token = match.group(1)
            print(f"تم العثور على توكن جديد: {new_token}")
        else:
            # توكن احتياطي إذا لم نجد في المصدر الأول
            new_token = "ugeen2024" 
            print("لم يتم العثور على توكن، استخدام التوكن الافتراضي.")

        # 2. قنواتك الـ VIP التي أرسلتها لي (سنقوم بتوليدها برمجياً مع التوكن الجديد)
        # سأضع لك أهم القنوات التي طلبتها (beIN و SSC) بنفس روابط ملفك
        channels = [
            {"name": "beIN SPORTS 1 EN", "id": "beIN_SPORTS_1_EN"},
            {"name": "beIN SPORTS 2 EN", "id": "beIN_SPORTS_2_EN"},
            {"name": "SSC 1 HD", "id": "SSC_1_HD"},
            {"name": "SSC 2 HD", "id": "SSC_2_HD"},
            {"name": "SSC EXTRA 1 HD", "id": "SSC_EXTRA_1_HD"}
        ]
        
        final_m3u = "#EXTM3U\n"
        base_url = "http://premium.ugeen.live:80/live/ugeen/ugeen/"
        
        for ch in channels:
            # دمج الرابط مع التوكن الجديد
            link = f"{base_url}{ch['id']}.m3u8?token={new_token}"
            final_m3u += f"#EXTINF:-1, {ch['name']}\n{link}\n"
            
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(final_m3u)
        print("تم تحديث ملف VIP بنجاح!")

    except Exception as e:
        print(f"حدث خطأ: {e}")

if __name__ == "__main__":
    update_ugeen_vip()
