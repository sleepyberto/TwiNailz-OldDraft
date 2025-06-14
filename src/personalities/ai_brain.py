import json
import random
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

from config import DATABASE_URL


@dataclass
class UserProfile:
    user_id: int
    preferred_styles: List[str]
    tone_preference: str  # 'elegant', 'bold', 'mixed'
    common_requests: List[str]
    interaction_count: int
    last_seen: datetime


class PersonalityCore:
    """Dual personality system for Lumi and Zae"""

    def __init__(self):
        self.lumi_traits = {
            "tone": "calm, elegant, sophisticated",
            "style_preference": ["minimalist", "nude", "classic", "subtle", "refined"],
            "phrases": [
                "Let's keep it elegant with",
                "For sophisticated beauty, try",
                "Timeless and refined",
                "Classic never goes out of style",
                "Understated elegance calls for",
            ],
        }

        self.zae_traits = {
            "tone": "bold, playful, trendy",
            "style_preference": [
                "colorful",
                "dramatic",
                "glitter",
                "artistic",
                "statement",
            ],
            "phrases": [
                "Let's go bold with",
                "Turn heads with this",
                "Ready to make a statement?",
                "Color me obsessed with",
                "Drama level: Maximum!",
            ],
        }

    def choose_personality(self, user_profile: UserProfile, request_type: str) -> str:
        """Choose dominant personality based on user preferences and request"""
        if user_profile.tone_preference == "elegant":
            return "lumi"
        elif user_profile.tone_preference == "bold":
            return "zae"

        # Mixed or new user - choose based on request keywords
        bold_keywords = ["bold", "bright", "colorful", "dramatic", "statement", "party"]
        elegant_keywords = [
            "elegant",
            "subtle",
            "classic",
            "minimal",
            "work",
            "professional",
        ]

        request_lower = request_type.lower()
        if any(keyword in request_lower for keyword in bold_keywords):
            return "zae"
        elif any(keyword in request_lower for keyword in elegant_keywords):
            return "lumi"

        return random.choice(["lumi", "zae"])


class PhraseEvolution:
    """Manages phrase packs and learning behavior"""

    def __init__(self):
        self.base_phrases = {
            "intro": [
                "For a bold statement, try",
                "Keep it classy with",
                "You'll love this if you're feeling",
                "This design screams sophistication:",
                "Want to turn heads? Then this is it:",
                "Let your nails do the talking with",
            ],
            "pairing": [
                "Pair this with gold rings for a goddess vibe",
                "Stack some delicate rings for the perfect finish",
                "Add a subtle bracelet to complete the look",
            ],
            "care_tips": ["Pro tip from Lumi:", "Zae's secret:", "Don't forget to"],
        }

        self.evolved_phrases = {}
        self.phrase_usage_count = {}

    def get_evolved_phrase(self, category: str, user_profile: UserProfile) -> str:
        """Get an evolved phrase based on usage patterns"""
        base_options = self.base_phrases.get(category, [])

        # Check if we have evolved phrases for this user
        user_key = f"{user_profile.user_id}_{category}"
        if user_key in self.evolved_phrases:
            # Mix evolved and base phrases
            all_options = base_options + self.evolved_phrases[user_key]
        else:
            all_options = base_options

        if not all_options:
            return "Let's try"

        # Choose phrase and track usage
        chosen = random.choice(all_options)
        self.phrase_usage_count[chosen] = self.phrase_usage_count.get(chosen, 0) + 1

        return chosen

    def evolve_phrase(self, original: str) -> List[str]:
        """Create variations of successful phrases"""
        evolution_patterns = {
            "For a bold statement, try": [
                "If you're going loud, try",
                "Ready for some drama? Try",
                "Bold vibes call for",
            ],
            "Keep it classy with": [
                "Stay elegant with",
                "Timeless beauty needs",
                "Classic charm requires",
            ],
            "You'll love this if you're feeling": [
                "Perfect when you're in the mood for",
                "Ideal if you're craving",
                "Just right when you want",
            ],
        }

        return evolution_patterns.get(original, [original])


class NailKnowledgeBase:
    """Expert nail knowledge and trend awareness"""

    def __init__(self):
        self.nail_shapes = {
            "oval": "Classic and versatile, flattering on most hand shapes",
            "round": "Natural and low-maintenance, perfect for short nails",
            "square": "Bold and modern, great for nail art",
            "coffin": "Trendy and dramatic, requires longer nails",
            "almond": "Elegant and elongating, sophisticated choice",
            "stiletto": "Bold and edgy, maximum drama",
        }

        self.color_psychology = {
            "red": "confidence, power, classic elegance",
            "pink": "feminine, soft, romantic",
            "nude": "versatile, professional, timeless",
            "black": "edgy, mysterious, statement-making",
            "white": "clean, minimalist, modern",
            "blue": "calming, unique, creative",
        }

        self.seasonal_trends = {
            "spring": ["pastel pink", "mint green", "lavender", "coral"],
            "summer": ["bright coral", "ocean blue", "sunny yellow", "tropical"],
            "fall": ["burgundy", "burnt orange", "deep plum", "golden bronze"],
            "winter": ["deep red", "emerald green", "silver", "midnight blue"],
        }

    def generate_design_name(self, colors: List[str], style: str) -> str:
        """Create creative names for nail designs"""
        elegant_adjectives = [
            "Aurora",
            "Velvet",
            "Starlight",
            "Diamond",
            "Pearl",
            "Silk",
        ]
        bold_adjectives = ["Electric", "Cosmic", "Neon", "Fire", "Thunder", "Galaxy"]

        endings = ["Bloom", "Spark", "Tips", "Dream", "Glow", "Magic", "Vibe"]

        if "elegant" in style.lower() or "minimal" in style.lower():
            adj = random.choice(elegant_adjectives)
        else:
            adj = random.choice(bold_adjectives)

        end = random.choice(endings)
        return f"{adj} {end}"


class TwiNailzBrain:
    """Main AI brain orchestrating all components"""

    def __init__(self):
        self.personality = PersonalityCore()
        self.phrases = PhraseEvolution()
        self.knowledge = NailKnowledgeBase()
        self.user_profiles = {}
        self._init_database()

    def _init_database(self):
        """Initialize SQLite database for interaction logging"""
        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                request_text TEXT,
                response_text TEXT,
                personality_used TEXT,
                phrases_used TEXT,
                timestamp DATETIME,
                user_rating INTEGER
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_preferences (
                user_id INTEGER PRIMARY KEY,
                preferred_styles TEXT,
                tone_preference TEXT,
                common_requests TEXT,
                interaction_count INTEGER,
                last_seen DATETIME
            )
        """
        )

        conn.commit()
        conn.close()

    def get_user_profile(self, user_id: int) -> UserProfile:
        """Retrieve or create user profile"""
        if user_id in self.user_profiles:
            return self.user_profiles[user_id]

        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM user_preferences WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()

        if result:
            profile = UserProfile(
                user_id=result[0],
                preferred_styles=json.loads(result[1]) if result[1] else [],
                tone_preference=result[2] or "mixed",
                common_requests=json.loads(result[3]) if result[3] else [],
                interaction_count=result[4] or 0,
                last_seen=(
                    datetime.fromisoformat(result[5]) if result[5] else datetime.now()
                ),
            )
        else:
            profile = UserProfile(
                user_id=user_id,
                preferred_styles=[],
                tone_preference="mixed",
                common_requests=[],
                interaction_count=0,
                last_seen=datetime.now(),
            )

        conn.close()
        self.user_profiles[user_id] = profile
        return profile

    def generate_response(self, user_id: int, request: str) -> Dict[str, str]:
        """Generate personalized nail advice response"""
        user_profile = self.get_user_profile(user_id)
        personality = self.personality.choose_personality(user_profile, request)

        # Get appropriate phrases
        intro_phrase = self.phrases.get_evolved_phrase("intro", user_profile)

        # Generate nail design suggestion based on request
        design_name = self.knowledge.generate_design_name(["pink", "gold"], request)

        # Build response with personality blend
        if personality == "lumi":
            response = (
                f"Lumi's suggestion: {intro_phrase} a sophisticated {design_name}. "
            )
            response += "Keep your cuticles oiled for that extra gloss glow. ✨"
        else:
            response = f"Zae's pick: {intro_phrase} a bold {design_name}! "
            response += "We're going all out with this one! 💥"

        # Add tagline
        response += "\n\n— TwiNailz: Two minds. One glam obsession. 💅"

        # Log interaction
        self._log_interaction(user_id, request, response, personality, [intro_phrase])

        return {
            "response": response,
            "personality": personality,
            "design_name": design_name,
        }

    def _log_interaction(
        self,
        user_id: int,
        request: str,
        response: str,
        personality: str,
        phrases: List[str],
    ):
        """Log interaction for learning purposes"""
        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO user_interactions 
            (user_id, request_text, response_text, personality_used, phrases_used, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                user_id,
                request,
                response,
                personality,
                json.dumps(phrases),
                datetime.now(),
            ),
        )

        # Update user profile
        user_profile = self.user_profiles.get(user_id)
        if user_profile:
            user_profile.interaction_count += 1
            user_profile.last_seen = datetime.now()

            cursor.execute(
                """
                INSERT OR REPLACE INTO user_preferences 
                (user_id, preferred_styles, tone_preference, common_requests, interaction_count, last_seen)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    user_id,
                    json.dumps(user_profile.preferred_styles),
                    user_profile.tone_preference,
                    json.dumps(user_profile.common_requests),
                    user_profile.interaction_count,
                    user_profile.last_seen.isoformat(),
                ),
            )

        conn.commit()
        conn.close()

    def learn_from_feedback(self, user_id: int, interaction_id: int, rating: int):
        """Learn from user feedback to improve responses"""
        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE user_interactions 
            SET user_rating = ? 
            WHERE id = ? AND user_id = ?
        """,
            (rating, interaction_id, user_id),
        )

        conn.commit()
        conn.close()

        # If high rating, evolve successful phrases
        if rating >= 4:
            # Get the phrases used in this interaction
            cursor.execute(
                "SELECT phrases_used FROM user_interactions WHERE id = ?",
                (interaction_id,),
            )
            result = cursor.fetchone()
            if result:
                phrases = json.loads(result[0])
                for phrase in phrases:
                    evolved = self.phrases.evolve_phrase(phrase)
                    # Store evolved phrases for this user
                    user_key = f"{user_id}_intro"
                    if user_key not in self.phrases.evolved_phrases:
                        self.phrases.evolved_phrases[user_key] = []
                    self.phrases.evolved_phrases[user_key].extend(evolved)


# Initialize the AI brain
twinailz_brain = TwiNailzBrain()
