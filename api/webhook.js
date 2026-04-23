const TelegramBot = require('node-telegram-bot-api');
const AuthService = require('../auth-vercel'); // Use Vercel specific auth
const SubscriptionService = require('../subscription');

// إعداد البوت بدون Polling لأن Vercel تعمل بنظام Webhook
const bot = new TelegramBot(process.env.TELEGRAM_BOT_TOKEN);
const apiBaseUri = 'http://176.123.9.60:3000';
const websiteUri = 'http://ugeen.live';

const authService = new AuthService(websiteUri);
const subService = new SubscriptionService(apiBaseUri, authService);

module.exports = async (request, response) => {
    try {
        const body = request.body;

        if (body && body.message) {
            const chatId = body.message.chat.id;
            const text = body.message.text;

            if (text === '/start') {
                await bot.sendMessage(chatId, '👋 أهلاً بك! البوت يعمل الآن على Vercel.\nأرسل /create لإنشاء حساب.');
            }
            else if (text === '/create') {
                await bot.sendMessage(chatId, '⚙️ جاري إنشاء الحساب (Vercel)... قد يستغرق وقتاً أطول قليلاً.');
                try {
                    // Logic here...
                    // سنقوم بنسخ المنطق من bot.js لاحقاً أو تحويله لملف مشترك
                    const username = `ugeen_${Math.random().toString(36).substring(7)}`;
                    const password = Math.random().toString(36).substring(2, 12);
                    const email = `${username}@gmail.com`;

                    await authService.register(username, email, password);
                    await bot.sendMessage(chatId, `✅ تم التسجيل!\nU: ${username}\nP: ${password}`);
                } catch (e) {
                    await bot.sendMessage(chatId, `❌ خطأ: ${e.message}`);
                }
            }
        }
    } catch (error) {
        console.error('Error sending message', error);
    }

    response.status(200).send('OK');
};
