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
from personalities import nail_personalities  # Import the sophisticated system

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TwiNailzBot:
    def __init__(self):
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
        nail_db.add_user_sync(user.id, user.username, user.first_name)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        message_text = update.message.text.strip()

        try:
            # 🔧 FIXED: Use the sophisticated personality system correctly!
            response = nail_personalities.get_response(message_text, user_id=user_id)
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

    # 🗑️ REMOVED: The duplicate _generate_contextual_response method
    # Now using the sophisticated personalities system instead!

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
        print("🚀 TwiNailz.AI Bot Starting...")
        print("✅ Database initialized")
        print("✅ Personalities system loaded")
        print("🤖 Bot is now running...")
        self.app.run_polling()


if __name__ == "__main__":
    bot = TwiNailzBot()
    bot.run()
