import requests

def get_link():
    # هذا الرابط هو الرابط المباشر الذي يسحب منه الموقع ملفاته عادة
    # قمت بتخمين المسار الأكثر شيوعاً للموقع
    direct_url = "http://ugeen.live/ugeen.m3u" 
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(direct_url, headers=headers, timeout=15)
        
        # التأكد أن الملف المسحوب هو ملف قنوات حقيقي
        if "#EXTM3U" in response.text:
            with open("playlist.m3u", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("نجاح! تم سحب ملف القنوات الحقيقي.")
        else:
            print("لم يتم العثور على #EXTM3U، جاري محاولة الرابط البديل...")
            # محاولة رابط بديل آخر
            alt_url = "http://ugeen.live/download.php"
            # (هنا يمكن إضافة المزيد من المحاولات إذا لزم الأمر)
            
    except Exception as e:
        print(f"خطأ: {e}")

if __name__ == "__main__":
    get_link()
