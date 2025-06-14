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
from personalities import nail_personalities

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TwiNailzBot:
    def __init__(self):
        if not BOT_TOKEN:
            raise ValueError("❌ BOT_TOKEN not found! Check your .env file")

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
🌟 **Lumi** - Elegant, sophisticated, caring
🔥 **Zae** - Bold, trendy, energetic

Just tell me what you're looking for! Try:
*"I need nails for a birthday party"*
*"My nails break easily"*
*"Show me some red nail ideas"*"""

        keyboard = [
            [InlineKeyboardButton("💅 Get Design Ideas", callback_data="designs")],
            [InlineKeyboardButton("🎨 Current Trends", callback_data="trends")],
            [InlineKeyboardButton("💊 Nail Care Tips", callback_data="care")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            welcome_message, reply_markup=reply_markup, parse_mode="Markdown"
        )

        # Add user to database
        try:
            nail_db.add_user_sync(user.id, user.username, user.first_name)
        except Exception as e:
            logger.error(f"Database error: {e}")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        message_text = update.message.text.strip()

        try:
            # Use the sophisticated personality system correctly
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

            # Save conversation
            try:
                nail_db.save_conversation_sync(
                    user_id, message_text, response, "contextual"
                )
            except Exception as e:
                logger.error(f"Database save error: {e}")

        except Exception as e:
            logger.error(f"Error: {e}")
            await update.message.reply_text(
                "Oops! Something went glam-wrong 💅 Please try again!"
            )

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        if query.data == "designs":
            await query.edit_message_text(
                "✨ Tell me what occasion or style you're looking for! 💅"
            )
        elif query.data == "trends":
            trends_text = """🔥 **Current Trends:**
• Chrome & mirror finishes
• Minimalist line art
• Abstract patterns
• Glass skin effect nails

What trend interests you? 💅"""
            await query.edit_message_text(trends_text)
        elif query.data == "care":
            care_text = """💊 **Daily Care Tips:**
• Apply cuticle oil morning & night
• Moisturize hands after washing
• Use glass file only
• Wear gloves for cleaning

Any specific nail concerns? 💅"""
            await query.edit_message_text(care_text)
        elif query.data.startswith("rate_"):
            await query.edit_message_text("Thanks for the rating! 💅✨")

    def run(self):
        print("🚀 TwiNailz.AI Bot Starting...")
        print("✅ Checking database...")
        print("✅ Loading personalities...")
        print("🤖 Bot is now running...")
        self.app.run_polling()


if __name__ == "__main__":
    try:
        bot = TwiNailzBot()
        bot.run()
    except Exception as e:
        print(f"❌ Bot failed to start: {e}")
        print("Check your .env file and BOT_TOKEN!")
