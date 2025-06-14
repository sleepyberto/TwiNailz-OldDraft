import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN
from database import nail_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WELCOME_MESSAGE = """💅 **Welcome to TwiNailz.AI!** ✨

Meet your twin nail consultants:
🌟 **Lumi** - Elegant, sophisticated, minimalist luxury
🔥 **Zae** - Bold, trendy, colorful and creative

Just tell me what you're looking for! Try:
*"I need nails for a birthday party"*
*"My nails break easily"*
*"Show me red nail ideas"*"""

PARTY_RESPONSE = """🎉 **Party nails coming up!**

🌟 **Lumi suggests:** Champagne chrome with gold accents!
🔥 **Zae says:** Holographic glitter with neon accents!

**Quick Options:**
• Glitter gradient
• Metallic chrome  
• Neon accent nail
• Rhinestone details"""


class TwiNailzBot:
    def __init__(self):
        if not BOT_TOKEN or len(BOT_TOKEN) < 10:
            raise ValueError("Invalid BOT_TOKEN configuration")
        self.app = Application.builder().token(BOT_TOKEN).build()
        self.setup_handlers()

    def setup_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )
        self.app.add_handler(CallbackQueryHandler(self.handle_callback))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user

        welcome_message = """💅 **Welcome to TwiNailz.AI!** ✨

Meet your twin nail consultants:
🌟 **Lumi** - Elegant, sophisticated, minimalist luxury
🔥 **Zae** - Bold, trendy, colorful and creative

Just tell me what you're looking for! Try:
*"I need nails for a birthday party"*
*"My nails break easily"*
*"Show me red nail ideas"*"""

        keyboard = [
            [InlineKeyboardButton("💅 Get Design Ideas", callback_data="designs")],
            [InlineKeyboardButton("🎨 Seasonal Trends", callback_data="trends")],
            [InlineKeyboardButton("💊 Nail Care Tips", callback_data="care")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            welcome_message, reply_markup=reply_markup, parse_mode="Markdown"
        )
        await nail_db.add_user(user.id, user.username, user.first_name)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        message_text = update.message.text.lower().strip()

        try:
            response = self._generate_response(message_text)
            response += "\n\n— TwiNailz: Two minds. One glam obsession. 💎"

            keyboard = [
                [InlineKeyboardButton("⭐⭐⭐⭐⭐", callback_data="rate_5")],
                [InlineKeyboardButton("🎨 More Ideas", callback_data="designs")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                response, reply_markup=reply_markup, parse_mode="Markdown"
            )
            nail_db.save_conversation_sync(
                user_id, message_text, response, "contextual"
            )

        except Exception as e:
            logger.error(f"Error: {e}")
            await update.message.reply_text(
                "Oops! Something went glam-wrong 💅 Please try again!"
            )

    RESPONSE_HANDLERS = {
        "party": (["party", "birthday", "celebration"], "_get_party_response"),
        "work": (["work", "office", "professional"], "_get_work_response"),
        "color": (["red", "blue", "pink", "color"], "_get_color_response"),
    }

    def _generate_response(self, message_text):
        for category, (keywords, handler_name) in RESPONSE_HANDLERS.items():
            if any(word in message_text for word in keywords):
                return getattr(self, handler_name)()
        return self._get_default_response()

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        if query.data == "designs":
            await query.edit_message_text(
                "✨ Tell me what occasion or style you're looking for! 💅"
            )
        elif query.data == "trends":
            await query.edit_message_text(
                "🔥 **Current Trends:** Chrome finishes, glass skin nails, abstract art! 💅"
            )
        elif query.data == "care":
            await query.edit_message_text(
                "💊 **Daily Care:** Cuticle oil, moisturize, gentle filing! 💅"
            )
        elif query.data.startswith("rate_"):
            await query.edit_message_text("Thanks for the rating! 💅✨")

    def run(self):
        print(" TwiNailz.AI Bot Starting...")
        print("✅ Database initialized")
        print("🤖 Bot is now running...")
        self.app.run_polling()


if __name__ == "__main__":
    bot = TwiNailzBot()
    bot.run()
