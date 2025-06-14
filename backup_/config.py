import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL", "twinailz_data.db")

# Nail knowledge configuration
NAIL_TRENDS_API = os.getenv("NAIL_TRENDS_API", None)
BEAUTY_SOURCES = [
    "https://www.nailpro.com",
    "https://www.allure.com/topic/nails",
    "https://www.pinterest.com/search/pins/?q=nail%20inspiration",
]
