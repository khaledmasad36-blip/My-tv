import requests
import re

def get_active_ugeen_links():
    # هذه الصفحة يقوم مبرمجون بتحديثها بـ "توكن" شغال ليوجين كل ساعة
    # نحن سنقوم بـ "قنص" التوكن منها ونضعه في روابطك
    source_url = "https://raw.githubusercontent.com/fomny/iptv/main/ugeen.m3u"
    
    try:
        response = requests.get(source_url, timeout=10).text
        # استخراج التوكن الشغال حالياً باستخدام Regex
        token_match = re.search(r'token=([a-zA-Z0-9]+)', response)
        
        if token_match:
            active_token = token_match.group(1)
            print(f"تم العثور على مفتاح شغال: {active_token}")
            
            # روابط قنواتك الـ VIP (beIN و SSC و Alwan)
            # هذه الروابط هي المحرك الأساسي ليوجين
            channels = [
                {"n": "beIN SPORTS 1 HD", "id": "3019"},
                {"n": "beIN SPORTS 2 HD", "id": "3020"},
                {"n": "SSC 1 HD", "id": "1331"},
                {"n": "ALWAN Sports 1", "id": "4661"},
                {"n": "ALWAN Sports 2", "id": "4662"}
            ]
            
            m3u_content = "#EXTM3U\n"
            base = "http://ugeen.live:8080/live/Ugeen_VIPtaT6Z3/QgRQ1c/"
            
            for ch in channels:
                # ندمج رابط قناتك مع المفتاح الشغال الذي سرقناه
                m3u_content += f"#EXTINF:-1, {ch['n']}\n{base}{ch['id']}.ts?token={active_token}\n"
            
            with open("playlist.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_content)
            print("تم تحديث الملف بمفتاح جديد!")
        else:
            print("لم نجد مفتاحاً شغالاً حالياً.")
            
    except Exception as e:
        print(f"خطأ في الاتصال: {e}")

if __name__ == "__main__":
    get_active_ugeen_links()
