import requests

def update_final():
    # هذا الرابط هو أقوى مصدر حالي للقنوات العربية والرياضية المحدثة
    url = "https://raw.githubusercontent.com/MoXmo/IPTV/main/Arab.m3u"
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code == 200 and "#EXTM3U" in response.text:
            # حفظ الملف كما هو لضمان عمل كل القنوات
            with open("playlist.m3u", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("نجاح! تم سحب مئات القنوات الرياضية.")
        else:
            print("المصدر لم يستجب بشكل صحيح، جاري محاولة مصدر بديل...")
            # مصدر بديل احتياطي
            alt_url = "https://iptv-org.github.io/iptv/languages/ara.m3u"
            response_alt = requests.get(alt_url, headers=headers, timeout=20)
            with open("playlist.m3u", "w", encoding="utf-8") as f:
                f.write(response_alt.text)

    except Exception as e:
        print(f"خطأ في الاتصال: {e}")

if __name__ == "__main__":
    update_final()
