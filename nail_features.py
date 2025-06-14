import random
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List


class NailShape(Enum):
    OVAL = "oval"
    ROUND = "round"
    SQUARE = "square"
    COFFIN = "coffin"
    ALMOND = "almond"
    STILETTO = "stiletto"
    SQUOVAL = "squoval"


class Occasion(Enum):
    EVERYDAY = "everyday"
    WORK = "work"
    PARTY = "party"
    WEDDING = "wedding"
    DATE = "date"
    VACATION = "vacation"
    FORMAL = "formal"


@dataclass
class NailRecommendation:
    design_name: str
    colors: List[str]
    shape: NailShape
    finish: str
    difficulty: int
    occasion: Occasion
    description: str
    care_tips: List[str]
    personality_source: str


class TwiNailzFeatures:
    """Complete nail expertise system"""

    def __init__(self):
        self.seasonal_colors = {
            "spring": ["soft pink", "mint green", "lavender", "peach"],
            "summer": ["bright coral", "ocean blue", "sunny yellow", "hot pink"],
            "fall": ["burgundy", "burnt orange", "deep plum", "gold"],
            "winter": ["deep red", "emerald green", "silver", "navy blue"],
        }

        self.design_names = {
            "elegant": ["Aurora", "Pearl", "Silk", "Diamond", "Velvet", "Starlight"],
            "bold": ["Electric", "Neon", "Fire", "Thunder", "Cosmic", "Galaxy"],
            "endings": ["Dream", "Glow", "Spark", "Tips", "Magic", "Vibe", "Shine"],
        }

    def get_recommendation(self, request_data: Dict) -> NailRecommendation:
        """Generate complete nail recommendation"""

        occasion = Occasion(request_data.get("occasion", "everyday"))
        personality = request_data.get("personality", "lumi")

        # Generate design name
        if personality == "lumi":
            adj = random.choice(self.design_names["elegant"])
        else:
            adj = random.choice(self.design_names["bold"])

        ending = random.choice(self.design_names["endings"])
        design_name = f"{adj} {ending}"

        # Get seasonal colors
        season = self._get_current_season()
        colors = random.sample(self.seasonal_colors[season], 2)

        return NailRecommendation(
            design_name=design_name,
            colors=colors,
            shape=NailShape.OVAL,
            finish="glossy" if personality == "lumi" else "matte",
            difficulty=2,
            occasion=occasion,
            description=f"A beautiful {personality}-inspired design perfect for {occasion.value}",
            care_tips=["Apply base coat", "Use cuticle oil daily"],
            personality_source=personality,
        )

    def _get_current_season(self) -> str:
        month = datetime.now().month
        if month in [3, 4, 5]:
            return "spring"
        elif month in [6, 7, 8]:
            return "summer"
        elif month in [9, 10, 11]:
            return "fall"
        else:
            return "winter"


# Initialize features
nail_features = TwiNailzFeatures()
