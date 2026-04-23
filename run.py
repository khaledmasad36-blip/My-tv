import requests

# بياناتك (يجب وضعها كـ Secrets في GitHub للأمان)
EMAIL = "khaledmasad36@gmail.com"
PASS = "هنا_باسورد_الموقع" # الباسورد اللي تدخل فيه الموقع
CODE = "Ugeen_VIPtaV6Z3"

def run_task():
    session = requests.Session() # استخدام Session يحافظ على الكوكيز والتوكن آلياً
    
    # 1. تسجيل الدخول والحصول على التوكن
    login_data = {"email": EMAIL, "password": PASS}
    login_res = session.post("http://176.123.9.60:3000/v1/auth/login", json=login_data)
    
    if login_res.status_code != 200:
        print("❌ فشل الدخول.. تأكد من بيانات الحساب")
        return

    token = login_res.json()['token']
    session.headers.update({'Authorization': f'Bearer {token}'})

    # 2. الحصول على توكن التفعيل المؤقت
    res_temp = session.post("http://176.123.9.60:3000/v1/codes")
    if res_temp.status_code == 200:
        temp_token = res_temp.json()['code']['token']
        
        # 3. التفعيل النهائي
        payload = {'code': CODE, 'token': temp_token, 'bouquetId': '1'}
        res_final = session.post("http://176.123.9.60:3000/v1/subscriptions/guests", json=payload)
        
        if res_final.status_code in [200, 201]:
            print("✅ تم التجديد بنجاح من سيرفر GitHub!")
        elif res_final.status_code == 422:
            print("ℹ️ السيرفر يقول: الاشتراك فعال حالياً.")
    else:
        print("❌ فشل الحصول على توكن التفعيل")

if __name__ == "__main__":
    run_task()
