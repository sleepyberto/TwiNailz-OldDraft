#!/usr/bin/env python3
"""
🚀 TwiNailz.AI Bot Launcher
Launch your nail beauty consultant bot!
"""
import logging
import sys

from telegram_bot import main

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def check_requirements():
    """Check if all requirements are met"""
    try:
        from config import BOT_TOKEN

        if not BOT_TOKEN:
            print("❌ Error: TELEGRAM_BOT_TOKEN not found in .env file!")
            return False
        print("✅ Bot token found")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False


if __name__ == "__main__":
    print("💅 ✨ TwiNailz.AI Starting Up ✨ 💅")
    print("=" * 40)

    if not check_requirements():
        print("\n🛠️  Fix the issues above and try again!")
        sys.exit(1)

    try:
        print("🚀 Launching TwiNailz.AI bot...")
        print("🌟 Lumi & Zae are ready to serve!")
        print("💎 Press Ctrl+C to stop the bot")
        print("=" * 40)

        main()

    except KeyboardInterrupt:
        print("\n👋 TwiNailz.AI stopped gracefully")
        print("💅 Thanks for using TwiNailz!")

    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        print("🛠️  Check your configuration and try again")
        sys.exit(1)
