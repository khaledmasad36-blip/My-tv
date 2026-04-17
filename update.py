import requests

def get_link():
    url = "http://ugeen.live"
    # إضافة معلومات متصفح حقيقي لتجنب الحظر
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            with open("playlist.m3u", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("نجح استخراج الملف!")
        else:
            print(f"فشل الموقع في الاستجابة: {response.status_code}")
    except Exception as e:
        print(f"حدث خطأ تقني: {e}")

if __name__ == "__main__":
    get_link()
