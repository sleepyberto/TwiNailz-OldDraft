import logging
import random
import sqlite3
from datetime import datetime

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


class TwiNailzBot:
    def __init__(self, token: str):
        self.token = token
        self.init_database()
        self.load_phrases()
        self.load_nail_knowledge()

    def init_database(self):
        """Initialize SQLite database for interaction logging"""
        self.conn = sqlite3.connect("twinailz_data.db", check_same_thread=False)
        cursor = self.conn.cursor()

        # User interactions table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                message TEXT,
                response_type TEXT,
                timestamp DATETIME,
                phrases_used TEXT
            )
        """
        )

        # User preferences table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_preferences (
                user_id INTEGER PRIMARY KEY,
                preferred_style TEXT,
                common_requests TEXT,
                tone_preference TEXT,
                nail_shapes TEXT,
                colors_liked TEXT
            )
        """
        )

        self.conn.commit()

    def load_phrases(self):
        """Load starter phrases and learning patterns"""
        self.starter_phrases = {
            "bold": [
                "For a bold statement, try...",
                "If you're going loud, try...",
                "Want to turn heads? Then this is it:",
                "Let your nails do the talking with...",
                "Ready to serve looks? Here's your moment:",
            ],
            "elegant": [
                "Keep it classy with...",
                "This design screams sophistication:",
                "For timeless elegance, go with...",
                "Channel your inner goddess with...",
                "Understated luxury vibes:",
            ],
            "playful": [
                "You'll love this if you're feeling...",
                "For that fun-loving energy, try...",
                "Playful meets pretty with...",
                "Bring out your wild side:",
                "Sweet meets sassy:",
            ],
        }

        self.design_names = [
            "Aurora Bloom",
            "Velvet Spark",
            "Starlight Tips",
            "Cosmic Dust",
            "Pearl Whisper",
            "Midnight Rose",
            "Golden Hour",
            "Ocean Breeze",
            "Sunset Glow",
            "Diamond Dreams",
            "Ruby Romance",
            "Lavender Haze",
        ]

    def load_nail_knowledge(self):
        """Load nail care and design knowledge base"""
        self.nail_shapes = {
            "oval": "Classic and flattering for most hand shapes",
            "square": "Bold and modern, great for strong nails",
            "round": "Natural and low-maintenance",
            "coffin": "Trendy and dramatic, perfect for statement nails",
            "almond": "Elegant and elongating for fingers",
        }

        self.seasonal_trends = {
            "spring": ["pastel pinks", "mint green", "lavender", "coral"],
            "summer": ["bright orange", "ocean blue", "sunset yellow", "hot pink"],
            "fall": ["burgundy", "burnt orange", "deep purple", "forest green"],
            "winter": ["deep red", "icy blue", "silver", "midnight black"],
        }

        self.nail_care_tips = {
            "brittle": "Use cuticle oil daily, avoid harsh acetone, try biotin supplements",
            "breaking": "File in one direction, use a base coat, keep nails hydrated",
            "growth": "Massage cuticles, eat protein-rich foods, be gentle with your nails",
        }


class PersonalityMixer:
    """Handles the dual personality responses"""

    @staticmethod
    def get_lumi_response(content: str) -> str:
        """Lumi's calm, elegant response style"""
        lumi_starters = [
            "Lumi suggests:",
            "From Lumi's perspective:",
            "Lumi's wisdom:",
            "Lumi whispers:",
            "Lumi's elegant choice:",
        ]
        return f"{random.choice(lumi_starters)} {content}"

    @staticmethod
    def get_zae_response(content: str) -> str:
        """Zae's bold, playful response style"""
        zae_starters = [
            "Zae's pick?",
            "Zae says:",
            "Zae's bold choice:",
            "Zae's vibe:",
            "Zae is obsessed with:",
        ]
        return f"{random.choice(zae_starters)} {content}"

    @staticmethod
    def get_mixed_response(lumi_content: str, zae_content: str) -> str:
        """Combine both personalities"""
        return f"{PersonalityMixer.get_zae_response(zae_content)} {PersonalityMixer.get_lumi_response(lumi_content)}"


class NailAdvisor:
    def __init__(self, bot_instance):
        self.bot = bot_instance
        self.personality = PersonalityMixer()

    def generate_design_recommendation(self, user_request: str, user_id: int) -> str:
        """Generate personalized nail design recommendations"""

        # Analyze user request for keywords
        request_lower = user_request.lower()

        # Determine style preference
        if any(
            word in request_lower
            for word in ["bold", "dramatic", "statement", "bright"]
        ):
            style_type = "bold"
        elif any(
            word in request_lower
            for word in ["elegant", "classy", "sophisticated", "minimal"]
        ):
            style_type = "elegant"
        else:
            style_type = "playful"

        # Get appropriate starter phrase
        starter = random.choice(self.bot.starter_phrases[style_type])

        # Generate design name
        design_name = random.choice(self.bot.design_names)

        # Create recommendation based on request context
        if "birthday" in request_lower:
            zae_rec = "Soft rose-pink ombré with heart decals on the middle fingers — we're going flirty and fun!"
            lumi_advice = "Keep your cuticles oiled for that extra gloss glow."
            response = f"{starter} {self.personality.get_mixed_response(lumi_advice, zae_rec)} Name this one: Birthday Blush. 💖"

        elif any(word in request_lower for word in ["break", "brittle", "weak"]):
            advice = self.bot.nail_care_tips.get(
                "breaking", "Focus on nail health first!"
            )
            response = f"Lumi's advice: {advice} Strong nails, strong energy. ✨"

        else:
            # General recommendation
            response = f"{starter} {design_name} — a perfect blend of style and personality! 💅"

        # Log interaction
        self.log_interaction(user_id, user_request, response, style_type)

        return f"{response}\n\n— TwiNailz: Two minds. One glam obsession."

    def log_interaction(
        self, user_id: int, message: str, response: str, response_type: str
    ):
        """Log user interactions for learning"""
        cursor = self.bot.conn.cursor()
        cursor.execute(
            """
            INSERT INTO interactions (user_id, message, response_type, timestamp, phrases_used)
            VALUES (?, ?, ?, ?, ?)
        """,
            (user_id, message, response_type, datetime.now(), response),
        )
        self.bot.conn.commit()


# Initialize bot instance
twinailz = TwiNailzBot("YOUR_BOT_TOKEN_HERE")
advisor = NailAdvisor(twinailz)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler"""
    welcome_msg = """
💅 Hey gorgeous! Welcome to TwiNailz! 💅

I'm your AI nail beauty consultant powered by twins Lumi & Zae:
✨ Lumi brings elegant, minimalist wisdom
🌈 Zae serves bold, trendy creativity

Ready to create some nail magic? Just tell me:
• What occasion are you styling for?
• Your mood or vibe
• Any specific colors or styles you love

Let's make your nails absolutely stunning! 💫

— TwiNailz: Two minds. One glam obsession.
    """
    await update.message.reply_text(welcome_msg)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user messages and generate responses"""
    user_message = update.message.text
    user_id = update.effective_user.id

    # Generate personalized response
    response = advisor.generate_design_recommendation(user_message, user_id)

    await update.message.reply_text(response)


def main():
    """Main function to run the bot"""
    application = Application.builder().token(twinailz.token).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    # Run the bot
    application.run_polling()


if __name__ == "__main__":
    main()
