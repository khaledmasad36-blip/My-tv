require('dotenv').config();
const TelegramBot = require('node-telegram-bot-api');
const AuthService = require('./auth');
const SubscriptionService = require('./subscription');

// Config
const telegramToken = process.env.TELEGRAM_BOT_TOKEN;
const baseUri = 'http://176.123.9.60:3000';

if (!telegramToken) {
    console.error('❌ Telegram Token Missing in .env');
    process.exit(1);
}

// Initialize Services
const bot = new TelegramBot(telegramToken, { polling: true });
const authService = new AuthService(baseUri);
const subService = new SubscriptionService(baseUri, authService);

console.log('🚀 Ugeen Bot Started (Modular Version)...');

// --- Command Handlers ---

// Helper: Generate Random String
const randomString = (length) => Math.random().toString(36).substring(2, 2 + length);

bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    const welcomeMsg = `
👋 *أهلاً بك في بوت Ugeen المطور*

ماذا تريد أن تفعل؟
1️⃣ /create - إنشاء حساب جديد
2️⃣ /info - عرض بيانات اشتراكك
3️⃣ /code - جلب كود تفعيل فقط
4️⃣ /renew - تجديد الاشتراك تلقائياً ⚡
    `;
    bot.sendMessage(chatId, welcomeMsg, { parse_mode: 'Markdown' });
});

bot.onText(/\/create/, async (msg) => {
    const chatId = msg.chat.id;
    const waitMsg = await bot.sendMessage(chatId, '⚙️ جاري إنشاء الحساب...');

    try {
        const username = `ugeen_${randomString(8)}`;
        const password = randomString(10);
        const email = `${username}@gmail.com`;

        await authService.register(username, email, password);
        await bot.editMessageText('✅ تم التسجيل! جاري تسجيل الدخول...', { chat_id: chatId, message_id: waitMsg.message_id });

        const token = await authService.login(username, password);

        let infoText = '';
        try {
            const info = await subService.getSubscriptionDetails();
            // تخمين هيكلة البيانات بناء على HTML
            // user-id, iptv-user, iptv-pass
            // سنعرض الـ JSON بالكامل للمستخدم في البداية لتسهيل التصحيح
            /* 
               IMPORTANT: Since we inferred the endpoint, exact JSON structure is unknown.
               We will dump the useful parts we find or the whole object if small.
            */
            const iptvUser = info.user?.username || info.iptv_user || info.username || 'N/A';
            const iptvPass = info.user?.password || info.iptv_pass || info.password || 'N/A';

            infoText = `
📺 *بيانات IPTV:*
👤 User: \`${iptvUser}\`
🔐 Pass: \`${iptvPass}\`
Host: \`${info.server?.host || 'ugeen.tv'}\`
           `;
        } catch (e) {
            infoText = '\n⚠️ لم نتمكن من جلب تفاصيل الاشتراك تلقائياً.';
        }

        const reply = `
🎉 *تم إنشاء الحساب بنجاح!*

📧 Email: \`${email}\`
🔑 Pass: \`${password}\`
👤 User: \`${username}\`

${infoText}

💡 لتجديد الاشتراك أرسل /renew
        `;

        bot.sendMessage(chatId, reply, { parse_mode: 'Markdown' });

    } catch (error) {
        console.error(error);
        bot.sendMessage(chatId, `❌ فشل إنشاء الحساب.\nالسبب: ${error.response?.data?.message || error.message}`);
    }
});

bot.onText(/\/code/, async (msg) => {
    const chatId = msg.chat.id;
    const waitMsg = await bot.sendMessage(chatId, '⏳ جاري الاتصال بالسيرفر...');

    try {
        const code = await subService.getRenewalCode();

        const reply = `
✅ *تم جلب الكود بنجاح!*

🔑 الكود: \`${code}\`
        `;

        bot.deleteMessage(chatId, waitMsg.message_id);
        bot.sendMessage(chatId, reply, { parse_mode: 'Markdown' });

    } catch (error) {
        let errorMsg = '❌ فشل العملية.';
        if (error.response?.status === 401) errorMsg += ' (تسجيل الدخول مطلوب)';

        bot.deleteMessage(chatId, waitMsg.message_id);
        bot.sendMessage(chatId, errorMsg);
    }
});

bot.onText(/\/info/, async (msg) => {
    const chatId = msg.chat.id;
    if (!authService.isAuthenticated()) {
        return bot.sendMessage(chatId, '⛔ يجب عليك تسجيل الدخول أو إنشاء حساب أولاً /create');
    }

    const waitMsg = await bot.sendMessage(chatId, '⏳ جاري جلب البيانات...');
    try {
        const info = await subService.getSubscriptionDetails();
        // Assuming structure based on similar panels
        const reply = `
📋 *بيانات الاشتراك:*

👤 User: \`${info.user?.username || info.iptv_user || 'غير موجود'}\`
🔐 Pass: \`${info.user?.password || info.iptv_pass || 'غير موجود'}\`
📅 Expire: \`${info.expire_date || info.subscription?.expire || 'غير محدد'}\`

_ملاحظة: إذا كانت البيانات غير دقيقة، هذا بسبب أننا نخمن شكل الرد من السيرفر_
        `;
        bot.deleteMessage(chatId, waitMsg.message_id);
        bot.sendMessage(chatId, reply, { parse_mode: 'Markdown' });
    } catch (error) {
        bot.deleteMessage(chatId, waitMsg.message_id);
        bot.sendMessage(chatId, `❌ فشل جلب البيانات: ${error.message}`);
    }
});

bot.onText(/\/renew/, async (msg) => {
    const chatId = msg.chat.id;
    if (!authService.isAuthenticated()) {
        return bot.sendMessage(chatId, '⛔ يجب عليك تسجيل الدخول أو إنشاء حساب أولاً /create');
    }

    const waitMsg = await bot.sendMessage(chatId, '⚡ جاري التجديد التلقائي...');

    try {
        // 1. Get Code
        const code = await subService.getRenewalCode();
        await bot.editMessageText(`✅ تم جلب الكود: ${code}\n⏳ جاري التفعيل...`, { chat_id: chatId, message_id: waitMsg.message_id });

        // 2. Renew
        await subService.renewSubscription(code);

        const reply = `
✅ *تم تجديد الاشتراك بنجاح!* 🚀

الآن يمكنك استخدام بياناتك في /info للمشاهدة.
        `;
        bot.sendMessage(chatId, reply, { parse_mode: 'Markdown' });

    } catch (error) {
        bot.sendMessage(chatId, `❌ فشل التجديد: ${error.message}`);
    }
});
