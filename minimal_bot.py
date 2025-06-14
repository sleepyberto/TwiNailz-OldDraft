import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💅✨ Welcome to TwiNailz.AI! ✨💅\n"
        "Your AI nail beauty consultant is ready!\n\n"
        "Commands:\n"
        "/trends - Get current nail trends\n"
        "/colors - Seasonal color recommendations\n"
        "/help - Show all commands"
    )


async def trends(update: Update, context: ContextTypes.DEFAULT_TYPE):
    trends_msg = (
        "🔥 Current Nail Trends:\n\n"
        "• Chrome & Mirror Finishes\n"
        "• Minimalist French Tips\n"
        "• Ombre & Gradient Effects\n"
        "• Geometric Patterns\n"
        "• Matte Top Coats\n\n"
        "Which style interests you most? 💅"
    )
    await update.message.reply_text(trends_msg)


async def colors(update: Update, context: ContextTypes.DEFAULT_TYPE):
    colors_msg = (
        "🎨 Seasonal Colors:\n\n"
        "🌸 Spring: Soft pinks, mint green, lavender\n"
        "☀️ Summer: Coral, turquoise, bright yellow\n"
        "🍂 Fall: Burgundy, burnt orange, deep plum\n"
        "❄️ Winter: Deep red, emerald, silver\n\n"
        "What season are you feeling? ✨"
    )
    await update.message.reply_text(colors_msg)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("trends", trends))
    app.add_handler(CommandHandler("colors", colors))

    print("🚀 TwiNailz.AI Bot Starting...")
    app.run_polling()


if __name__ == "__main__":
    main()
