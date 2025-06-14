from datetime import datetime

from pytrends.request import TrendReq


class NailTrendsAPI:
    """Enhanced trends using Google Trends + scraping"""

    def __init__(self):
        self.pytrends = TrendReq(hl="en-US", tz=360)

    def get_trending_nail_searches(self) -> dict:
        """Get trending nail searches from Google"""
        try:
            # Nail-related keywords
            keywords = [
                "nail art",
                "nail design",
                "nail color",
                "nail trends",
                "manicure",
            ]
            self.pytrends.build_payload(keywords, cat=0, timeframe="today 3-m")

            # Get interest over time
            trends_data = self.pytrends.interest_over_time()

            # Get related queries
            related = self.pytrends.related_queries()

            return {
                "trending_searches": (
                    trends_data.to_dict() if not trends_data.empty else {}
                ),
                "related_queries": related,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            print(f"Trends API error: {e}")
            return {"error": str(e)}

    def get_seasonal_predictions(self) -> dict:
        """Predict seasonal trends"""
        season_keywords = {
            "spring": ["pastel nails", "floral nail art", "spring manicure"],
            "summer": ["bright nails", "neon nails", "beach nails"],
            "fall": ["autumn nails", "burgundy nails", "fall colors"],
            "winter": ["holiday nails", "glitter nails", "winter manicure"],
        }

        current_month = datetime.now().month
        if current_month in [3, 4, 5]:
            season = "spring"
        elif current_month in [6, 7, 8]:
            season = "summer"
        elif current_month in [9, 10, 11]:
            season = "fall"
        else:
            season = "winter"

        return {
            "current_season": season,
            "predicted_trends": season_keywords[season],
            "confidence": "high",
        }


# Initialize trends API
nail_trends_api = NailTrendsAPI()
