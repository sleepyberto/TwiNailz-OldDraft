import logging
import sqlite3
from datetime import datetime

logger = logging.getLogger(__name__)


class NailDatabase:
    def __init__(self, db_path: str = "twinailz_data.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize database with required tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Users table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    personality_preference TEXT DEFAULT 'lumi',
                    interaction_count INTEGER DEFAULT 0
                )
            """
            )

            # Conversations table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    message TEXT,
                    response TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    personality TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """
            )

            # Nail trends cache
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS trends_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    trend_data TEXT,
                    cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP
                )
            """
            )

            conn.commit()
            conn.close()
            logger.info("✅ Database initialized successfully")

        except Exception as e:
            logger.error(f"❌ Database initialization error: {e}")
            raise

    def add_user_sync(self, user_id: int, username: str = None, first_name: str = None):
        """Add new user to database (sync version)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO users (user_id, username, first_name, last_active) VALUES (?, ?, ?, ?)",
                (user_id, username, first_name, datetime.now()),
            )
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error adding user: {e}")

    def get_user_sync(self, user_id: int):
        """Get user data (sync version)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()
            conn.close()
            return result
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            return None

    def save_conversation_sync(
        self, user_id: int, message: str, response: str, personality: str
    ):
        """Save conversation to database (sync version)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO conversations (user_id, message, response, personality) VALUES (?, ?, ?, ?)",
                (user_id, message, response, personality),
            )
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error saving conversation: {e}")


# Initialize database
nail_db = NailDatabase()
