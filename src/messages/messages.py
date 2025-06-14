class MessageTemplates:
    """Centralized message templates for the bot"""

    def __init__(self):
        self.signature = "\n\n— TwiNailz: Two minds. One glam obsession. 💎"

    def get_welcome_message(self):
        return """💅 **Welcome to TwiNailz.AI!** ✨

Meet your twin nail consultants:
🌟 **Lumi** - Elegant, sophisticated, minimalist luxury
🔥 **Zae** - Bold, trendy, colorful and creative

**What can I help you with?**
• Expert nail design ideas for any occasion
• Color recommendations for your skin tone  
• Professional nail care advice & health tips
• Seasonal trend insights
• Custom design creation with creative names

Just tell me what you're looking for! Try:
*"I need nails for a birthday brunch"*
*"My nails break too easily"*
*"Show me fall trends"*

— TwiNailz: Two minds. One glam obsession. 💎"""

    def get_design_options_message(self):
        return "💅 **What's the occasion?**\nChoose the vibe that matches your energy:"

    def get_seasonal_trends_message(self):
        return """🍂 **Current Trends**

**🎨 Hot Colors:**
• Burgundy & Deep Reds
• Gold & Copper Metallics  
• Rich Forest Greens

**✨ Popular Themes:**
• Elegant Minimalism
• Festive Sparkles
• Cozy Earth Tones

**💎 Trending Finishes:**
• Matte Textures
• Chrome Effects
• Glossy Topcoats

Ready to try one of these trends? Just ask me!"""

    def get_care_tips_message(self):
        return """💊 **Professional Nail Care Tips**

**Daily Essentials:**
• Apply cuticle oil morning & night
• Moisturize hands after washing
• Wear gloves for cleaning

**Weekly Routine:**
• File nails with glass file only
• Push back cuticles gently
• Apply strengthening base coat

**Pro Tips from Lumi & Zae:**
🌟 *Lumi*: "Consistency is key - small daily steps create beautiful results"
🔥 *Zae*: "Don't forget to show your nails some love - they work hard!"

**Need specific help?** Tell me about your nail concerns!"""

    def get_inspiration_message(self):
        return """✨ **Quick Inspiration Boost!**

**Today's Vibe:**
🌟 *Lumi suggests*: "Soft nude with a single accent nail in rose gold"
🔥 *Zae suggests*: "Electric blue with holographic tips - be bold!"

**Color of the Day:** Deep Plum 🍇
**Technique Spotlight:** Gradient ombre effects

Ready for a custom design? Just ask!"""

    def get_design_message(self, design_type: str) -> str:
        designs = {
            "party": """🎉 **Party Perfect Nails!**
            
🌟 *Lumi's Elegant Choice*: "Rose gold glitter gradient with nude base"
🔥 *Zae's Bold Pick*: "Holographic rainbow with chrome accents"

**Perfect for:** Birthdays, celebrations, nights out
**Duration:** 2-3 weeks with proper care""",
            "work": """💼 **Professional Polish**
            
🌟 *Lumi's Classic*: "Soft ballet pink with subtle shimmer"
🔥 *Zae's Modern*: "Matte navy with gold accent stripe"

**Perfect for:** Office, meetings, professional events
**Benefits:** Chip-resistant, long-lasting""",
            "date": """💕 **Date Night Drama**
            
🌟 *Lumi's Romance*: "Dusty rose with pearl details"
🔥 *Zae's Statement*: "Deep burgundy with gold foil art"

**Perfect for:** Romantic dinners, special occasions
**Mood:** Confidence and elegance""",
            "wedding": """👰 **Bridal Beauty**
            
🌟 *Lumi's Timeless*: "Classic French with pearl accents"
🔥 *Zae's Glam*: "Soft pink with delicate lace design"

**Perfect for:** Weddings, formal events
**Photo-ready:** Guaranteed to look stunning in pictures""",
        }

        return designs.get(design_type, "Custom design coming right up! 💅✨")

    def get_signature(self):
        return self.signature

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            user = update.effective_user
            user_id = user.id

            self.user_sessions[user_id] = {
                "stage": "welcome",
                "preferences": {},
                "last_suggestions": [],
                "interaction_count": 0,
            }

            welcome_message = """💅✨ **Welcome to TwiNailz.AI!** ✨💅
            
Meet your twin nail consultants:
🌟 **Lumi** - Sophisticated elegance specialist
🔥 **Zae** - Bold creativity expert
            
**I'm your AI nail guru that can:**
• Create custom design ideas 🎨"""

            await update.message.reply_text(welcome_message)

        except Exception as e:
            logger.error(f"Error in start_command: {str(e)}")
            await update.message.reply_text(
                "Sorry, something went wrong. Please try again later."
            )
