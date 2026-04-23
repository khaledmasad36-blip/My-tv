const axios = require('axios');

class AuthService {
    constructor(baseUri) {
        this.baseUri = baseUri;
        this.currentUser = null;
        this.token = process.env.UGEEN_JWT || null;
    }

    async register(username, email, password) {
        console.log("⚙️ Starting Puppeteer for registration...");
        const puppeteer = require('puppeteer-extra');
        const StealthPlugin = require('puppeteer-extra-plugin-stealth');
        puppeteer.use(StealthPlugin());

        let browser;
        try {
            browser = await puppeteer.launch({
                headless: "new", // تشغيل بالخلفية
                args: ['--no-sandbox', '--disable-setuid-sandbox']
            });
            const page = await browser.newPage();

            // تحسين الأداء
            await page.setRequestInterception(true);
            page.on('request', (req) => {
                if (['image', 'stylesheet', 'font'].includes(req.resourceType())) {
                    req.abort();
                } else {
                    req.continue();
                }
            });

            console.log("🌍 Navigating to signup page...");
            await page.goto(`${this.baseUri}/signup.html`, { waitUntil: 'networkidle2' });

            // ملء البيانات
            console.log("✍️ Filling form...");
            await page.type('#name', username);
            await page.type('#email', email);
            await page.type('#password', password);

            // النقر على زر التسجيل وانتظار الانتقال لصفحة تسجيل الدخول
            console.log("🖱️ Clicking Signup...");

            await Promise.all([
                page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 20000 }), // ننتظر الانتقال
                page.click('#submit')
            ]);

            console.log("✅ Registration Successful (Navigated)");
            return { success: true };

        } catch (error) {
            console.error("Puppeteer Registration Error:", error.message);
            // محاولة التقاط صورة للخطأ إذا فشل
            // if (browser) await page.screenshot({ path: 'error.png' });
            throw new Error(`Registration Failed: ${error.message}`);
        } finally {
            if (browser) await browser.close();
        }
    }

    async login(username, password) {
        console.log("⚙️ Starting Puppeteer for login...");
        const puppeteer = require('puppeteer-extra');
        const StealthPlugin = require('puppeteer-extra-plugin-stealth');
        puppeteer.use(StealthPlugin());

        let browser;
        try {
            browser = await puppeteer.launch({
                headless: "new",
                args: ['--no-sandbox', '--disable-setuid-sandbox']
            });
            const page = await browser.newPage();

            await page.setRequestInterception(true);
            page.on('request', (req) => {
                if (['image', 'stylesheet', 'font'].includes(req.resourceType())) {
                    req.abort();
                } else {
                    req.continue();
                }
            });

            console.log("🌍 Navigating to signin page...");
            await page.goto(`${this.baseUri}/signin.html`, { waitUntil: 'networkidle2' });

            console.log("✍️ Filling login form...");
            await page.type('#email', username); // في صفحة الدخول، الـ ID هو #email لكن يقبل username أيضاً حسب تجربتنا، أو سنستخدم Selector أدق
            // التصحيح: في signup كان id="name". في signin غالباً الحقل الأول
            // للتأكد سنستخدم input[type="text"] أو input[name="username"] لو وجد.
            // لكن لاحظت في كود الـ signup المرفق سابقاً: id="name"
            // سأفترض هنا أن المستخدم سيداريه البوت.
            // *تصحيح*: في صفحة الدخول في المواقع المشابهة يكون الـ ID غالباً 'email' أو 'username'.
            // سأجرب الكتابة في الحقل الأول الموجود.

            const emailInput = await page.$('input[type="text"]') || await page.$('input[type="email"]');
            if (emailInput) await emailInput.type(username);

            await page.type('input[type="password"]', password);

            console.log("🖱️ Clicking Login...");

            // التقاط الاستجابة للبحث عن التوكن
            const tokenPromise = new Promise((resolve, reject) => {
                page.on('response', async (response) => {
                    if (response.url().includes('/auth/login') && response.status() === 200) {
                        try {
                            const data = await response.json();
                            if (data.token) resolve(data.token);
                        } catch (e) { }
                    }
                });
            });

            await Promise.all([
                page.click('#submit') || page.click('button[type="submit"]'),
                // لا ننتظر الملاحة (navigation) فقط، بل ننتظر التوكن من الشبكة
            ]);

            // ننتظر التوكن بحد أقصى 10 ثواني
            const token = await Promise.race([
                tokenPromise,
                new Promise((_, reject) => setTimeout(() => reject(new Error("Timeout waiting for token")), 10000))
            ]);

            console.log("✅ Login Successful, Token retrieved.");
            this.token = token;
            this.currentUser = username;
            return token;

        } catch (error) {
            console.error("Puppeteer Login Error:", error.message);
            throw error;
        } finally {
            if (browser) await browser.close();
        }
    }

    // Temporary: Use existing token from env
    isAuthenticated() {
        return !!this.token;
    }

    getToken() {
        return this.token;
    }
}

module.exports = AuthService;
