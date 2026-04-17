import requests
import re

def get_real_link():
    url = "http://ugeen.live"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        # خطوة 1: دخول الموقع
        response = requests.get(url, headers=headers)
        # خطوة 2: البحث عن أي رابط ينتهي بـ .m3u داخل كود الموقع
        links = re.findall(r'https?://[^\s<>"]+\.m3u', response.text)
        
        if links:
            direct_link = links[0]
            # خطوة 3: تحميل ملف القنوات الحقيقي
            file_data = requests.get(direct_link, headers=headers)
            with open("playlist.m3u", "w", encoding="utf-8") as f:
                f.write(file_data.text)
            print("تم استخراج ملف القنوات بنجاح!")
        else:
            # إذا لم يجد رابط، سنسحب المحتوى ونحاول تنظيفه
            with open("playlist.m3u", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("تحذير: تم سحب الصفحة، قد تحتاج لتعديل الرابط المباشر")
    except Exception as e:
        print(f"خطأ: {e}")

if __name__ == "__main__":
    get_real_link()
