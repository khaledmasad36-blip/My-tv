import requests

def fix_everything():
    # هذا الرابط يحتوي على قنوات عربية مفتوحة ومضمونة 100%
    test_url = "https://iptv-org.github.io/iptv/languages/ara.m3u"
    
    try:
        response = requests.get(test_url, timeout=15)
        if response.status_code == 200:
            with open("playlist.m3u", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("تم تحديث الملف بنجاح!")
    except Exception as e:
        print(f"خطأ: {e}")

if __name__ == "__main__":
    fix_everything()
