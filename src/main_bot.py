#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TwiNailz.AI - Advanced Nail Care AI Bot"""

import asyncio
import logging
import os
import sys

# Load environment variables FIRST
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Bot configuration - Use environment variable directly
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN not found in .env file")
    sys.exit(1)
logger.info("Using BOT_TOKEN from environment variables")
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

from openai_handler import TwiNailzAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Add this temporary debug line after load_dotenv()
print(f"DEBUG: Bot token loaded: {os.getenv('TELEGRAM_BOT_TOKEN')[:10]}..." if os.getenv('TELEGRAM_BOT_TOKEN') else "DEBUG: No bot token found")


class TwiNailzBot:
    """Main bot class for TwiNailz.AI"""

    def __init__(self, token: str):
        self.token = token
        self.application = None
        self.nail_ai = TwiNailzAI()

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
        """Handle regular text messages with AI"""
        if update.message and update.message.text:
            user_message = update.message.text
        
            # Show typing indicator
            await update.message.reply_chat_action("typing")
        
            try:
                # Get AI response
                response = self.nail_ai.get_nail_recommendation(user_message)
                await update.message.reply_text(f"💅 {response}")
            except Exception as e:
                # Fallback to basic response
                if any(word in user_message.lower() for word in ["help", "advice", "tips"]):
                    await self.advice_command(update, context)
                else:
                    response = f"Thanks for your message! I'm TwiNailz.AI 💅\n\nUse /help to see what I can do for you!"
                    await update.message.reply_text(response)

    async def trends_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /trends command with AI"""
        if not update.message:
            return
    
        await update.message.reply_text("🔍 Getting the latest nail trends for you...")
    
        try:
            trends = self.nail_ai.get_nail_trends()
            await update.message.reply_text(f"✨ Current Nail Trends:\n\n{trends}")
        except Exception as e:
            await update.message.reply_text("Sorry, I couldn't get trends right now. Please try again later!")

    def setup_handlers(self):
        """Setup command and message handlers"""
        if not self.application:
            return
        # Add command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("advice", self.advice_command))
        self.application.add_handler(CommandHandler("trends", self.trends_command))
        # Add message handler
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )

    def run(self):
        """Run the bot"""
        try:
            # Create application
            self.application = Application.builder().token(self.token).build()
        
            # Setup handlers
            self.setup_handlers()
        
            logger.info("Starting TwiNailz.AI Bot...")
            logger.info("Bot is running! Press Ctrl+C to stop.")
        
            # Start the bot with polling (this handles all the async stuff)
            self.application.run_polling(allowed_updates=Update.ALL_TYPES)
        
        except Exception as e:
            logger.error(f"Error running bot: {e}")


def main():
    """Main function"""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not found")
        return
    
    bot = TwiNailzBot(BOT_TOKEN)
    try:
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
