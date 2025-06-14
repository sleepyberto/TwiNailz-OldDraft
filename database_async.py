import logging
from datetime import datetime

import aiosqlite

logger = logging.getLogger(__name__)


class AsyncNailDatabase:
    def __init__(self, db_path: str = "twinailz_data.db"):
        self.db_path = db_path

    async def init_database(self):
        """Initialize database with required tables (async)"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                # Users table
                await db.execute(
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
                await db.execute(
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

                # Trends cache
                await db.execute(
                    """
                    CREATE TABLE IF NOT EXISTS trends_cache (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        trend_data TEXT,
                        cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        expires_at TIMESTAMP
                    )
                """
                )

                await db.commit()
                logger.info("✅ Async Database initialized successfully")
        except Exception as e:
            logger.error(f"❌ Database initialization error: {e}")
            raise

    async def add_user(
        self, user_id: int, username: str = None, first_name: str = None
    ):
        """Add new user to database (async)"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "INSERT OR REPLACE INTO users (user_id, username, first_name, last_active) VALUES (?, ?, ?, ?)",
                    (user_id, username, first_name, datetime.now()),
                )
                await db.commit()
        except Exception as e:
            logger.error(f"Error adding user: {e}")

    async def save_conversation(
        self, user_id: int, message: str, response: str, personality: str
    ):
        """Save conversation to database (async)"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "INSERT INTO conversations (user_id, message, response, personality) VALUES (?, ?, ?, ?)",
                    (user_id, message, response, personality),
                )
                await db.commit()
        except Exception as e:
            logger.error(f"Error saving conversation: {e}")

    async def get_user_stats(self, user_id: int):
        """Get user statistics"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute(
                    "SELECT COUNT(*) as interaction_count FROM conversations WHERE user_id = ?",
                    (user_id,),
                )
                result = await cursor.fetchone()
                return result[0] if result else 0
        except Exception as e:
            logger.error(f"Error getting user stats: {e}")
            return 0


# Initialize async database
nail_db_async = AsyncNailDatabase()
