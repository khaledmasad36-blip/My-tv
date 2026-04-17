import requests
import concurrent.futures

def check_server(server_info):
    url, user, pw = server_info
    host = f"{url}/get.php?username={user}&password={pw}&type=m3u_plus&output=ts"
    try:
        # محاولة سحب القنوات بسرعة (timeout قصير لضمان السرعة)
        r = requests.get(host, timeout=5)
        if r.status_code == 200 and "#EXTM3U" in r.text:
            return r.text
    except:
        return None

def build_ugeen_style_list():
    # هذه قائمة "سيرفرات خام" (Raw Panels) يستخدمها كبار الموزعين
    # السكريبت سيجرب الدخول إليها وسحب باقة الرياضة وألوان
    potential_servers = [
        ("http://new.one-iptv.top:8080", "6565", "6565"),
        ("http://pure-iptv.com:8080", "111", "111"),
        ("http://line.hi-iptv.top:80", "demo", "demo"),
        ("http://p.f-iptv.com:8080", "66", "66")
    ]
    
    final_m3u = "#EXTM3U\n"
    keywords = ["BEIN", "SSC", "ALWAN", "AL KASS"]
    
    print("جاري البحث عن سيرفرات نشطة...")
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(check_server, potential_servers)
        
        for data in results:
            if data:
                lines = data.splitlines()
                for i in range(len(lines)):
                    if lines[i].startswith("#EXTINF"):
                        if any(k in lines[i].upper() for k in keywords):
                            final_m3u += lines[i] + "\n" + lines[i+1] + "\n"
                break # نتوقف عند أول سيرفر شغال لضمان الثبات

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_m3u)
    print("تم تحديث القائمة بنجاح!")

if __name__ == "__main__":
    build_ugeen_style_list()
