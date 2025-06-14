#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TwiNailz.AI - Advanced Nail Care AI Bot
"""

import asyncio
import logging
import os
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Bot configuration
try:
    from config import BOT_TOKEN
except ImportError:
    BOT_TOKEN = os.getenv("BOT_TOKEN", "your-bot-token-here")
    logger.warning("config.py not found, using environment variable")

# Try importing telegram bot
try:
    from telegram import Update
    from telegram.ext import (
        Application,
        CommandHandler,
        ContextTypes,
        MessageHandler,
        filters,
    )
except ImportError:
    logger.error(
        "python-telegram-bot not installed. Run: pip install python-telegram-bot"
    )
    sys.exit(1)


class TwiNailzBot:
    """Main bot class for TwiNailz.AI"""

    def __init__(self, token: str):
        self.token = token
        self.application = None

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        if not update.message:
            return

        welcome_message = """
🌟 Welcome to TwiNailz.AI! 🌟

Your AI-powered nail care assistant is here to help you achieve beautiful, healthy nails!

Available features:
• Personalized nail care advice
• Trend recommendations  
• Product suggestions
• Nail health analysis

Type /help to see all available commands!
        """
        await update.message.reply_text(welcome_message.strip())

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        if not update.message:
            return

        help_message = """
🛠️ TwiNailz.AI Commands:

/start - Welcome message
/help - Show this help
/advice - Get nail care advice
/trends - Latest nail trends
/analyze - Analyze your nails (send a photo)

Need specific help? Just ask me anything about nail care! 💅
        """
        await update.message.reply_text(help_message.strip())

    async def advice_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /advice command"""
        if not update.message:
            return

        advice = """
💡 Daily Nail Care Tips:

1. Keep nails clean and moisturized
2. Use a base coat before polish
3. Don't use nails as tools
4. Trim regularly with proper tools
5. Give nails a break from polish occasionally

What specific nail concern can I help you with?
        """
        await update.message.reply_text(advice.strip())

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages"""
        if update.message and update.message.text:
            user_message = update.message.text.lower()

            if any(word in user_message for word in ["help", "advice", "tips"]):
                await self.advice_command(update, context)
            else:
                response = f"Thanks for your message! I'm TwiNailz.AI 💅\n\nUse /help to see what I can do for you!"
                await update.message.reply_text(response)

    def setup_handlers(self):
        """Setup command and message handlers"""
        if not self.application:
            return

        # Add command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("advice", self.advice_command))

        # Add message handler
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )

    async def run(self):
        """Run the bot"""
        try:
            # Create application
            self.application = Application.builder().token(self.token).build()

            # Setup handlers
            self.setup_handlers()

            logger.info("Starting TwiNailz.AI Bot...")

            # Start the bot
            await self.application.initialize()
            await self.application.start()
            await self.application.updater.start_polling(
                allowed_updates=Update.ALL_TYPES
            )

            logger.info("Bot is running! Press Ctrl+C to stop.")

            # Keep running
            await self.application.updater.idle()

        except Exception as e:
            logger.error(f"Error running bot: {e}")
        finally:
            if self.application:
                await self.application.stop()


def main():
    """Main function"""
    if not BOT_TOKEN or BOT_TOKEN == "your-bot-token-here":
        logger.error("Please set your BOT_TOKEN in config.py or environment variable")
        return

    bot = TwiNailzBot(BOT_TOKEN)

    try:
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
