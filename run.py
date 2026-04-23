import requests

# بياناتك الثابتة
EMAIL = "khaledmasad36@gmail.com"
PASSWORD = "sehjiw-3Ducqo-poxxen"  # <--- حط باسوورد الموقع هنا
CODE = "Ugeen_VIPtaV6Z3"

def run_task():
    print("🚀 بدء عملية التفعيل التلقائي...")
    session = requests.Session()
    
    # الخطوة 1: تسجيل الدخول
    login_url = "http://176.123.9.60:3000/v1/auth/login"
    try:
        login_res = session.post(login_url, json={"email": EMAIL, "password": PASSWORD}, timeout=15)
        if login_res.status_code != 200:
            print(f"❌ فشل تسجيل الدخول: {login_res.status_code}")
            return
        
        token = login_res.json().get('token')
        print("✅ تم الحصول على التوكن الجديد.")
        session.headers.update({'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'})

        # الخطوة 2: طلب التوكن المؤقت
        res_temp = session.post("http://176.123.9.60:3000/v1/codes")
        if res_temp.status_code == 200:
            temp_token = res_temp.json()['code']['token']
            
            # الخطوة 3: التفعيل النهائي
            payload = {'code': CODE, 'token': temp_token, 'bouquetId': '1'}
            res_final = session.post("http://176.123.9.60:3000/v1/subscriptions/guests", json=payload)
            
            if res_final.status_code in [200, 201]:
                print("🎉 نجح التفعيل! الاشتراك جاهز.")
            elif res_final.status_code == 422:
                print("ℹ️ السيرفر يقول: الاشتراك مفعل مسبقاً ولا يحتاج تجديد الآن.")
        else:
            print("❌ فشل السيرفر في إصدار الكود المؤقت.")
            
    except Exception as e:
        print(f"❌ خطأ تقني: {e}")

if __name__ == "__main__":
    run_task()
