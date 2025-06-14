import asyncio
import hashlib
import logging
import os
import pickle
import sqlite3
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import aiohttp
import requests
from bs4 import BeautifulSoup

from config import DATABASE_URL, NAIL_TRENDS_API

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("twinailz.log"), logging.StreamHandler()],
)
logger = logging.getLogger("TwiNailz")


@dataclass
class APIResponse:
    success: bool
    data: Any
    error: Optional[str] = None
    cached: bool = False
    timestamp: datetime = None


class DatabaseManager:
    """Advanced SQLite database operations with connection pooling"""

    def __init__(self, db_path: str = DATABASE_URL):
        self.db_path = db_path
        self._init_tables()

    def _init_tables(self):
        """Initialize all required database tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # User profiles table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS user_profiles (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    preferred_styles TEXT,
                    tone_preference TEXT,
                    common_requests TEXT,
                    interaction_count INTEGER DEFAULT 0,
                    total_ratings REAL DEFAULT 0,
                    rating_count INTEGER DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_seen DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Interactions table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    message_id INTEGER,
                    request_text TEXT,
                    request_type TEXT,
                    response_text TEXT,
                    personality_used TEXT,
                    phrases_used TEXT,
                    design_generated TEXT,
                    processing_time REAL,
                    user_rating INTEGER,
                    feedback_text TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES user_profiles (user_id)
                )
            """
            )

            # Trends cache table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS trends_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT,
                    trend_type TEXT,
                    data TEXT,
                    hash_key TEXT UNIQUE,
                    expires_at DATETIME,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # System analytics table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name TEXT,
                    metric_value REAL,
                    metadata TEXT,
                    date DATE DEFAULT CURRENT_DATE
                )
            """
            )

            # Error logs table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS error_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    error_type TEXT,
                    error_message TEXT,
                    stack_trace TEXT,
                    user_id INTEGER,
                    context TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            conn.commit()
            logger.info("Database tables initialized successfully")

    @asynccontextmanager
    async def get_connection(self):
        """Async context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
        finally:
            conn.close()

    async def execute_query(
        self, query: str, params: tuple = (), fetch: str = None
    ) -> Any:
        """Execute database query with error handling"""
        try:
            async with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)

                if fetch == "one":
                    result = cursor.fetchone()
                elif fetch == "all":
                    result = cursor.fetchall()
                else:
                    result = cursor.rowcount

                conn.commit()
                return result
        except Exception as e:
            logger.error(f"Database query error: {e}")
            await self.log_error("DATABASE_ERROR", str(e), query)
            return None

    async def log_error(
        self, error_type: str, message: str, context: str = None, user_id: int = None
    ):
        """Log errors to database"""
        query = """
            INSERT INTO error_logs (error_type, error_message, context, user_id)
            VALUES (?, ?, ?, ?)
        """
        await self.execute_query(query, (error_type, message, context, user_id))


class CacheManager:
    """In-memory and persistent caching system"""

    def __init__(self, cache_dir: str = "cache/"):
        self.cache_dir = cache_dir
        self.memory_cache = {}
        self.cache_ttl = {}
        os.makedirs(cache_dir, exist_ok=True)

    def _get_cache_key(self, key: str) -> str:
        """Generate cache key hash"""
        return hashlib.md5(key.encode()).hexdigest()

    def set(self, key: str, data: Any, ttl_minutes: int = 60):
        """Set cache with TTL"""
        cache_key = self._get_cache_key(key)

        # Memory cache
        self.memory_cache[cache_key] = data
        self.cache_ttl[cache_key] = datetime.now() + timedelta(minutes=ttl_minutes)

        # Persistent cache
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
        try:
            with open(cache_file, "wb") as f:
                pickle.dump({"data": data, "expires": self.cache_ttl[cache_key]}, f)
        except Exception as e:
            logger.warning(f"Failed to write persistent cache: {e}")

    def get(self, key: str) -> Optional[Any]:
        """Get cached data"""
        cache_key = self._get_cache_key(key)

        # Check memory cache first
        if cache_key in self.memory_cache:
            if datetime.now() < self.cache_ttl.get(cache_key, datetime.now()):
                return self.memory_cache[cache_key]
            else:
                # Expired - remove from memory
                del self.memory_cache[cache_key]
                del self.cache_ttl[cache_key]

        # Check persistent cache
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, "rb") as f:
                    cached = pickle.load(f)
                    if datetime.now() < cached["expires"]:
                        # Restore to memory cache
                        self.memory_cache[cache_key] = cached["data"]
                        self.cache_ttl[cache_key] = cached["expires"]
                        return cached["data"]
                    else:
                        # Expired - remove file
                        os.remove(cache_file)
            except Exception as e:
                logger.warning(f"Failed to read persistent cache: {e}")

        return None

    def clear_expired(self):
        """Clear expired cache entries"""
        now = datetime.now()
        expired_keys = [k for k, ttl in self.cache_ttl.items() if now >= ttl]

        for key in expired_keys:
            if key in self.memory_cache:
                del self.memory_cache[key]
            del self.cache_ttl[key]

            # Remove persistent cache file
            cache_file = os.path.join(self.cache_dir, f"{key}.pkl")
            if os.path.exists(cache_file):
                try:
                    os.remove(cache_file)
                except Exception as e:
                    logger.warning(f"Failed to remove expired cache file: {e}")


class TrendScraper:
    """Web scraping for beauty trends from various sources"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": "TwiNailz-Bot/1.0 (Beauty Trend Analysis)"}
        )

    async def scrape_nail_pro(self) -> List[Dict]:
        """Scrape trends from NailPro.com"""
        try:
            response = self.session.get("https://www.nailpro.com/trends", timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")

            trends = []
            # Example scraping logic (adjust based on actual site structure)
            trend_articles = soup.find_all("article", class_="trend-item")[:5]

            for article in trend_articles:
                title = article.find("h2")
                description = article.find("p")

                if title and description:
                    trends.append(
                        {
                            "title": title.get_text().strip(),
                            "description": description.get_text().strip()[:200],
                            "source": "NailPro",
                            "scraped_at": datetime.now().isoformat(),
                        }
                    )

            return trends

        except Exception as e:
            logger.error(f"NailPro scraping error: {e}")
            return []

    async def scrape_allure_nails(self) -> List[Dict]:
        """Scrape nail trends from Allure"""
        try:
            response = self.session.get(
                "https://www.allure.com/topic/nails", timeout=10
            )
            soup = BeautifulSoup(response.content, "html.parser")

            trends = []
            # Example scraping logic
            articles = soup.find_all("div", class_="summary-item")[:3]

            for article in articles:
                title = article.find("h3")
                if title:
                    trends.append(
                        {
                            "title": title.get_text().strip(),
                            "source": "Allure",
                            "scraped_at": datetime.now().isoformat(),
                        }
                    )

            return trends

        except Exception as e:
            logger.error(f"Allure scraping error: {e}")
            return []

    async def get_all_trends(self) -> Dict[str, List]:
        """Aggregate trends from all sources"""
        tasks = [self.scrape_nail_pro(), self.scrape_allure_nails()]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        aggregated = {
            "nailpro": results[0] if not isinstance(results[0], Exception) else [],
            "allure": results[1] if not isinstance(results[1], Exception) else [],
            "last_updated": datetime.now().isoformat(),
        }

        return aggregated


class APIIntegration:
    """External API integrations and management"""

    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.rate_limits = {}

    async def call_nail_trends_api(
        self, endpoint: str, params: Dict = None
    ) -> APIResponse:
        """Call external nail trends API"""
        if not NAIL_TRENDS_API:
            return APIResponse(success=False, error="API key not configured")

        try:
            url = f"{NAIL_TRENDS_API}/{endpoint}"

            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return APIResponse(
                        success=True, data=data, timestamp=datetime.now()
                    )
                else:
                    return APIResponse(
                        success=False, error=f"API returned status {response.status}"
                    )

        except Exception as e:
            logger.error(f"API call error: {e}")
            return APIResponse(success=False, error=str(e))

    async def close(self):
        """Close HTTP session"""
        await self.session.close()


class PerformanceMonitor:
    """System performance monitoring and analytics"""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.metrics = {
            "requests_per_minute": [],
            "response_times": [],
            "error_counts": {},
            "user_satisfaction": [],
        }

    async def track_request(self, processing_time: float):
        """Track request processing time"""
        self.metrics["response_times"].append(processing_time)

        # Store in database for historical analysis
        await self.db.execute_query(
            "INSERT INTO analytics (metric_name, metric_value) VALUES (?, ?)",
            ("response_time", processing_time),
        )

    async def track_error(self, error_type: str):
        """Track error occurrence"""
        self.metrics["error_counts"][error_type] = (
            self.metrics["error_counts"].get(error_type, 0) + 1
        )

    async def track_satisfaction(self, rating: int):
        """Track user satisfaction ratings"""
        self.metrics["user_satisfaction"].append(rating)

        await self.db.execute_query(
            "INSERT INTO analytics (metric_name, metric_value) VALUES (?, ?)",
            ("user_rating", rating),
        )

    async def get_system_health(self) -> Dict:
        """Get system health metrics"""
        return {
            "avg_response_time": (
                sum(self.metrics["response_times"][-100:])
                / len(self.metrics["response_times"][-100:])
                if self.metrics["response_times"]
                else 0
            ),
            "error_rate": sum(self.metrics["error_counts"].values())
            / max(len(self.metrics["response_times"]), 1),
            "avg_satisfaction": (
                sum(self.metrics["user_satisfaction"][-50:])
                / len(self.metrics["user_satisfaction"][-50:])
                if self.metrics["user_satisfaction"]
                else 0
            ),
            "total_requests": len(self.metrics["response_times"]),
        }
