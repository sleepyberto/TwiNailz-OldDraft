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

**What can I help you with?**
• Expert nail design ideas for any occasion
• Color recommendations for your skin tone  
• Professional nail care advice & health tips
• Seasonal trend insights
• Custom design creation with creative names

Just tell me what you're looking for! Try:
*"I need nails for a birthday brunch"*
*"My nails break too easily"*
*"Show me fall trends"*

— TwiNailz: Two minds. One glam obsession. 💎"""

        keyboard = [
            [InlineKeyboardButton("💅 Get Design Ideas", callback_data="designs")],
            [InlineKeyboardButton("🎨 Seasonal Trends", callback_data="trends")],
            [InlineKeyboardButton("💊 Nail Care & Health", callback_data="care")],
            [InlineKeyboardButton("✨ Quick Inspiration", callback_data="inspiration")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            welcome_message, reply_markup=reply_markup, parse_mode="Markdown"
        )

        # Save user to database
        nail_db.add_user_sync(user.id, user.username, user.first_name)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Enhanced message handling with proper response formatting"""
        user_id = update.effective_user.id
        message_text = update.message.text

        try:
            # Get response from personalities
            response = nail_personalities.get_response(message_text)
            response += "\n\n— TwiNailz: Two minds. One glam obsession. 💎"

            # Add rating buttons
            keyboard = [
                [
                    InlineKeyboardButton("⭐", callback_data="rate_1"),
                    InlineKeyboardButton("⭐⭐", callback_data="rate_2"),
                    InlineKeyboardButton("⭐⭐⭐", callback_data="rate_3"),
                    InlineKeyboardButton("⭐⭐⭐⭐", callback_data="rate_4"),
                    InlineKeyboardButton("⭐⭐⭐⭐⭐", callback_data="rate_5"),
                ],
                [InlineKeyboardButton("🎨 Another Design", callback_data="designs")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                response, reply_markup=reply_markup, parse_mode="Markdown"
            )

            # Save conversation
            nail_db.save_conversation_sync(user_id, message_text, response, "auto")

        except Exception as e:
            logger.error(f"Message handling error: {e}")
            await update.message.reply_text(
                "Oops! Something went glam-wrong 💅 Please try again!"
            )

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()

        if query.data == "designs":
            await self._show_design_options(query)
        elif query.data == "trends":
            await self._show_seasonal_trends(query)
        elif query.data == "care":
            await self._show_care_tips(query)
        elif query.data.startswith("rate_"):
            rating = int(query.data.split("_")[1])
            await self._handle_rating(query, rating)

    async def _show_design_options(self, query):
        keyboard = [
            [InlineKeyboardButton("🎉 Party/Birthday", callback_data="design_party")],
            [InlineKeyboardButton("💼 Work/Professional", callback_data="design_work")],
            [InlineKeyboardButton("💕 Date Night", callback_data="design_date")],
            [InlineKeyboardButton("👰 Wedding/Formal", callback_data="design_wedding")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            "💅 **What's the occasion?**\nChoose the vibe that matches your energy:",
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )

    async def _show_seasonal_trends(self, query):
        """Show current seasonal trends"""
        trend_message = """🍂 **Current Trends**

**🎨 Hot Colors:**
• Burgundy & Deep Reds
• Gold & Copper Metallics  
• Rich Forest Greens

**✨ Popular Themes:**
• Elegant Minimalism
• Festive Sparkles
• Cozy Earth Tones

**💎 Trending Finishes:**
• Matte Textures
• Chrome Effects
• Glossy Topcoats

Ready to try one of these trends? Just ask me!"""

        keyboard = [
            [InlineKeyboardButton("🎨 Get Trend Design", callback_data="designs")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(trend_message, reply_markup=reply_markup)

    async def _show_care_tips(self, query):
        """Show nail care advice"""
        care_message = """💊 **Professional Nail Care Tips**

**Daily Essentials:**
• Apply cuticle oil morning & night
• Moisturize hands after washing
• Wear gloves for cleaning

**Weekly Routine:**
• File nails with glass file only
• Push back cuticles gently
• Apply strengthening base coat

**Pro Tips from Lumi & Zae:**
🌟 *Lumi*: "Consistency is key - small daily steps create beautiful results"
🔥 *Zae*: "Don't forget to show your nails some love - they work hard!"

**Need specific help?** Tell me about your nail concerns!"""

        keyboard = [
            [
                InlineKeyboardButton(
                    "💬 Ask About My Nails", callback_data="personal_care"
                )
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(care_message, reply_markup=reply_markup)

    async def _handle_rating(self, query, rating):
        """Handle user ratings"""
        await query.edit_message_text(f"Thanks for the {rating}⭐ rating! 💅✨")

    def run(self):
        print("🚀 TwiNailz.AI Bot Starting...")
        print("✅ Database initialized")
        print("🤖 Bot is now running...")
        self.app.run_polling()


if __name__ == "__main__":
    bot = TwiNailzBot()
    bot.run()
