from typing import List



class ProductRecommendations:
    """Product recommendations from beauty retailers"""

    def __init__(self):
        self.product_categories = {
            "base_coats": [
                "Essie Strong Start",
                "OPI Natural Nail Base Coat",
                "Sally Hansen Nail Rehab",
            ],
            "strengtheners": [
                "Sally Hansen Hard as Nails",
                "Essie Treat Love & Color",
                "OPI Nail Envy",
            ],
            "cuticle_oils": [
                "CND Solar Oil",
                "Burt's Bees Lemon Cuticle Cream",
                "Sally Hansen Vitamin E Oil",
            ],
            "top_coats": [
                "Seche Vite Dry Fast Top Coat",
                "Essie Good to Go",
                "OPI Top Coat",
            ],
            "tools": ["Glass nail file", "Cuticle pusher", "Buffer block"],
        }

    def get_recommendations(self, nail_concern: str) -> List[str]:
        """Get product recommendations for specific concerns"""
        if "brittle" in nail_concern or "weak" in nail_concern:
            return self.product_categories["strengtheners"]
