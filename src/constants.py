"""Constants and configuration messages for TwiNailz.AI Bot"""

# Bot Messages
WELCOME_MESSAGE = """💅 **Welcome to TwiNailz.AI!** ✨

Meet your twin nail consultants:
🌟 **Lumi** - Elegant, sophisticated, minimalist luxury
🔥 **Zae** - Bold, trendy, colorful and creative

Just tell me what you're looking for! Try:
*"I need nails for a birthday party"*
*"My nails break easily"*
*"Show me red nail ideas"*"""

PARTY_RESPONSE = """🎉 **Party nails coming up!**

🌟 **Lumi suggests:** Champagne chrome with gold accents!
🔥 **Zae says:** Holographic glitter with neon accents!

**Quick Options:**
• Glitter gradient
• Metallic chrome  
• Neon accent nail
• Rhinestone details"""

WORK_RESPONSE = """💼 **Professional nails that mean business!**

🌟 **Lumi recommends:** Nude with subtle shimmer
🔥 **Zae suggests:** Deep burgundy or navy

**Office Perfect:**
• Classic nude
• Soft pink
• Deep burgundy
• Navy blue"""

COLOR_RESPONSE = """🎨 **Color consultation time!**

🌟 **Lumi says:** Choose colors that make YOU confident!
🔥 **Zae adds:** Don't be afraid to try something new!

Tell me your skin tone and occasion for perfect recommendations! 🌈"""

DEFAULT_RESPONSE = """✨ **I'm here to help with all things nails!**

🌟 **Lumi:** Tell me your style preferences!
🔥 **Zae:** Give me any challenge!

**I can help with:**
• Design ideas
• Color recommendations  
• Nail care advice
• Trend updates

What specific nail question can I answer? 💅"""

BOT_SIGNATURE = "\n\n— TwiNailz: Two minds. One glam obsession. 💎"

# Keywords for response matching
RESPONSE_KEYWORDS = {
    "party": ["party", "birthday", "celebration", "event", "dance"],
    "work": ["work", "office", "professional", "meeting", "job", "corporate"],
    "color": [
        "red",
        "blue",
        "pink",
        "color",
        "black",
        "white",
        "green",
        "purple",
        "yellow",
    ],
}

# Button configurations
MAIN_MENU_BUTTONS = [
    [("💅 Get Design Ideas", "designs")],
    [("🎨 Seasonal Trends", "trends")],
    [("💊 Nail Care Tips", "care")],
]

RATING_BUTTONS = [[("⭐⭐⭐⭐⭐", "rate_5")], [("🎨 More Ideas", "designs")]]

# Error messages
ERROR_MESSAGES = {
    "general": "Oops! Something went glam-wrong 💅 Please try again!",
    "callback": "✨ Working on that feature! Try the main menu options! 💅",
    "database": "Sorry, having trouble saving that. Please try again! 💅",
}
