import requests

def update_playlist():
    # روابط مصادر قنوات موثوقة ومفتوحة (عربية وعالمية)
    sources = [
        "https://iptv-org.github.io/iptv/languages/ara.m3u", # قنوات عربية
        "https://raw.githubusercontent.com/MoXmo/IPTV/main/Arab.m3u" # مصدر عربي إضافي
    ]
    
    combined_content = "#EXTM3U\n"
    
    for url in sources:
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                # تنظيف المحتوى ودمجه
                lines = response.text.splitlines()
                if len(lines) > 1:
                    combined_content += "\n".join(lines[1:]) + "\n"
                print(f"تم سحب القنوات من: {url}")
        except:
            print(f"فشل سحب المصدر: {url}")

    # حفظ الملف النهائي
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(combined_content)
    print("تم تحديث ملفك بنجاح!")

if __name__ == "__main__":
    update_playlist()
