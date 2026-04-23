const axios = require('axios');

class AuthService {
    constructor(baseUri) {
        this.baseUri = baseUri;
        this.token = null;
        this.currentUser = null;
    }

    async register(username, email, password) {
        console.log("⚙️ Starting Puppeteer (Vercel Optimized)...");
        const puppeteer = require('puppeteer-core');
        const chromium = require('@sparticuz/chromium');

        let browser;
        try {
            // إعدادات خاصة لبيئة Vercel
            browser = await puppeteer.launch({
                args: chromium.args,
                defaultViewport: chromium.defaultViewport,
                executablePath: await chromium.executablePath(),
                headless: chromium.headless,
                ignoreHTTPSErrors: true,
            });

            const page = await browser.newPage();

            // Set User Agent to avoid detection
            await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');

            console.log("🌍 Navigating to signup page...");
            // Use networkidle0 to wait for all connections to finish
            await page.goto(`${this.baseUri}/signup.html`, { waitUntil: 'domcontentloaded', timeout: 60000 });

            const title = await page.title();
            const url = await page.url();
            console.log(`📄 Page Loaded: ${title} (${url})`);

            console.log("⏳ Waiting for form...");
            // Check if we are blocked or on a different page
            try {
                await page.waitForSelector('#name', { visible: true, timeout: 30000 });
            } catch (waitError) {
                console.error("❌ Selector not found. Dumping page content...");
                const content = await page.content();
                console.error("HTML Preview:", content.substring(0, 1000)); // Log first 1000 chars
                throw waitError;
            }

            console.log("✍️ Filling form...");
            await page.type('#name', username);
            await page.type('#email', email);
            await page.type('#password', password);

            console.log("🖱️ Clicking Signup...");

            // Click first
            await page.click('#submit');

            // Wait for URL to change to signin.html (Result of successful registration)
            // or timeout after 60s
            try {
                await page.waitForFunction(() => window.location.href.includes('signin.html'), { timeout: 60000 });
                console.log("✅ Registration Successful (Redirected to Signin)");
                return { success: true };
            } catch (e) {
                // Double check if we are already there
                if (page.url().includes('signin.html')) {
                    console.log("✅ Registration Successful (Redirected to Signin - Timeout Fallback)");
                    return { success: true };
                }
                console.error("❌ Registration Timeout. Current URL:", page.url());
                throw new Error("Registration timed out. Please try again.");
            }

        } catch (error) {
            console.error("Puppeteer Registration Error:", error.message);
            throw new Error(`Registration Failed: ${error.message}`);
        } finally {
            if (browser) await browser.close();
        }
    }

    async login(username, password) {
        // يمكن إضافة منطق الدخول هنا أيضاً باستخدام puppeteer-core بنفس الطريقة
        // للتبسيط حالياً سنتركها فارغة أو ننسخ المنطق عند الحاجة
        return { token: "dummy_token_vercel" };
    }
}

module.exports = AuthService;
