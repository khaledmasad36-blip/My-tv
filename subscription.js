const axios = require('axios');

class SubscriptionService {
    constructor(baseUri, authService) {
        this.baseUri = baseUri;
        this.authService = authService;
        this.apiVersion = 'v1';
    }

    async getRenewalCode() {
        if (!this.authService.isAuthenticated()) {
            throw new Error("User not authenticated");
        }

        try {
            const response = await axios.get(`${this.baseUri}/${this.apiVersion}/codes`, {
                headers: {
                    'Authorization': `Bearer ${this.authService.getToken()}`,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Referer': 'http://ugeen.live/'
                }
            });

            const downloadToken = response.data.token;
            const payloadPart = downloadToken.split('.')[1];
            const payload = JSON.parse(Buffer.from(payloadPart, 'base64').toString());

            return payload.code.code;
        } catch (error) {
            console.error("Fetch Code Error:", error.message);
            throw error;
        }
    }

    async renewSubscription(code, bouquetId = 385) {
        if (!this.authService.isAuthenticated()) {
            throw new Error("User not authenticated");
        }

        try {
            // نحتاج token الذي تم استخدامه لفك التشفير (downloadToken)
            // في الكود الحالي getRenewalCode تفك التشفير وتعيد الكود فقط
            // يجب علينا تخزين downloadToken مؤقتاً أو تعديل getRenewalCode لإعادته
            // للتبسيط، سنفترض أننا سنحصل عليه مرة أخرى أو نعدل getRenewalCode

            // *تعديل سريع*: سنقوم بطلب الكود مرة أخرى هنا داخلياً للحصول على التوكن
            // أو الأفضل: تمرير التوكن كـ argument.
            // الحل الأسرع: إعادة استدعاء logic جلب التوكن

            const codesResponse = await axios.get(`${this.baseUri}/${this.apiVersion}/codes`, {
                headers: {
                    'Authorization': `Bearer ${this.authService.getToken()}`,
                    'Referer': 'http://ugeen.live/renew.html'
                }
            });

            const downloadToken = codesResponse.data.token;

            console.log(`Renewing with Code: ${code} and Token: ${downloadToken.substring(0, 15)}...`);

            const response = await axios.post(`${this.baseUri}/${this.apiVersion}/subscriptions`, {
                bouquetId: bouquetId,
                code: code,
                token: downloadToken
            }, {
                headers: {
                    'Authorization': `Bearer ${this.authService.getToken()}`,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Referer': 'http://ugeen.live/renew.html',
                    'Content-Type': 'application/x-www-form-urlencoded' // jQuery $.post defaults to form-urlencoded often, checking... axios defaults to JSON. 
                    // في renew.js: data: object -> jQuery sends as form-urlencoded usually unless contentType is json.
                    // لكن headers تقول Accept: json. 
                    // لنجرب JSON أولاً لأنه المعيار الحديث، وإذا فشل نغيره.
                }
            });

            return response.data;
        } catch (error) {
            console.error("Renewal Error:", error.response?.data || error.message);
            throw error;
        }
    }

    async getSubscriptionDetails() {
        if (!this.authService.isAuthenticated()) {
            throw new Error("User not authenticated");
        }

        try {
            // تخمين: النقطة النهائية قد تكون /v1/subscription أو /v1/profile
            // بناءً على renew.js الذي يستخدم /subscriptions للتجديد
            const response = await axios.get(`${this.baseUri}/${this.apiVersion}/subscription`, {
                headers: {
                    'Authorization': `Bearer ${this.authService.getToken()}`,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Referer': 'http://ugeen.live/subscription.html'
                }
            });

            return response.data; // نتوقع أن يحتوي على iptv details
        } catch (error) {
            console.error("Get Info Error:", error.response?.data || error.message);
            throw error;
        }
    }
}

module.exports = SubscriptionService;
