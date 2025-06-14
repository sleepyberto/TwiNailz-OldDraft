

class ConversationContext:
    def __init__(self):
        self.user_contexts = {}  # Store context per user

    def get_context(self, user_id):
        if user_id not in self.user_contexts:
            self.user_contexts[user_id] = {
                "stage": "initial",
                "topic": None,
                "occasion": None,
                "preferences": {},
                "last_responses": [],
                "question_count": 0,
                "gathered_info": {},
            }
        return self.user_contexts[user_id]

    def update_context(self, user_id, **kwargs):
        context = self.get_context(user_id)
        context.update(kwargs)

    def add_response_history(self, user_id, response):
        context = self.get_context(user_id)
        context["last_responses"].append(response)
        if len(context["last_responses"]) > 5:  # Keep only last 5 responses
            context["last_responses"].pop(0)


class NailPersonalities:
    def __init__(self):
        self.conversation_context = ConversationContext()

        # Conversation stages for better flow
        self.conversation_stages = {
            "initial": "gathering_basic_info",
            "gathering_basic_info": "exploring_preferences",
            "exploring_preferences": "design_creation",
            "design_creation": "refinement",
            "refinement": "final_recommendation",
        }

        self.lumi_personality = {
            "style": "elegant, sophisticated, caring",
            "phrases": ["darling", "love", "dear", "beautiful soul"],
            "approach": "gentle guidance, refined suggestions",
        }

        self.zae_personality = {
            "style": "bold, energetic, trendy",
            "phrases": ["babe", "hun", "bestie", "queen"],
            "approach": "excited encouragement, bold ideas",
        }

    def get_response(self, message, user_id=None):
        """Generate contextual response based on conversation history"""
        if not user_id:
            user_id = "default"

        context = self.conversation_context.get_context(user_id)
        message_lower = message.lower()

        # Analyze the message
        analysis = self._analyze_message(message_lower, context)

        # Generate contextual response
        response = self._generate_contextual_response(
            message, analysis, context, user_id
        )

        # Update conversation context
        self._update_conversation_state(analysis, context, user_id)

        return response

    def _analyze_message(self, message, context):
        """Analyze message for intent, sentiment, and nail-related content"""
        analysis = {
            "contains_nail_terms": False,
            "sentiment": "neutral",
            "intent": "unknown",
            "occasion": None,
            "colors_mentioned": [],
            "problems_mentioned": [],
            "preferences_expressed": {},
        }

        # Check for nail-related terms
        nail_terms = ["nail", "manicure", "pedicure", "polish", "color", "design"]
        analysis["contains_nail_terms"] = any(term in message for term in nail_terms)

        # Detect sentiment
        positive_words = [
            "love",
            "like",
            "want",
            "need",
            "excited",
            "beautiful",
            "pretty",
        ]
        negative_words = ["hate", "don't like", "break", "chip", "ugly", "problem"]

        if any(word in message for word in positive_words):
            analysis["sentiment"] = "positive"
        elif any(word in message for word in negative_words):
            analysis["sentiment"] = "negative"

        # Detect intent
        if "?" in message or any(
            q in message for q in ["how", "what", "when", "where", "why"]
        ):
            analysis["intent"] = "question"
        elif any(word in message for word in ["want", "need", "looking for"]):
            analysis["intent"] = "request"
        elif any(word in message for word in ["yes", "no", "maybe", "sure"]):
            analysis["intent"] = "response"

        # Detect occasions
        occasions = {
            "work": ["work", "office", "professional", "meeting", "job"],
            "party": ["party", "birthday", "celebration", "club", "night out"],
            "date": ["date", "romantic", "dinner", "boyfriend", "girlfriend"],
            "wedding": ["wedding", "bride", "formal", "ceremony"],
        }

        for occasion, keywords in occasions.items():
            if any(keyword in message for keyword in keywords):
                analysis["occasion"] = occasion
                break

        # Extract colors mentioned
        colors = [
            "red",
            "blue",
            "pink",
            "black",
            "white",
            "gold",
            "silver",
            "purple",
            "green",
        ]
        analysis["colors_mentioned"] = [color for color in colors if color in message]

        # Check for problems
        problems = ["break", "chip", "weak", "brittle", "peel", "damage"]
        analysis["problems_mentioned"] = [
            problem for problem in problems if problem in message
        ]

        return analysis

    def _generate_contextual_response(self, message, analysis, context, user_id):
        """Generate response based on conversation context and stage"""
        stage = context["stage"]

        if stage == "initial":
            return self._handle_initial_contact(message, analysis, context)
        elif stage == "gathering_basic_info":
            return self._handle_info_gathering(message, analysis, context)
        elif stage == "exploring_preferences":
            return self._handle_preference_exploration(message, analysis, context)
        elif stage == "design_creation":
            return self._handle_design_creation(message, analysis, context)
        elif stage == "refinement":
            return self._handle_design_refinement(message, analysis, context)
        else:
            return self._handle_general_conversation(message, analysis, context)

    def _handle_initial_contact(self, message, analysis, context):
        """Handle first interaction - welcoming and basic info gathering"""
        if analysis["contains_nail_terms"] or analysis["occasion"]:
            lumi_response = f"Welcome, darling! ✨ I can see you're interested in {analysis['occasion'] or 'nail care'} - how exciting!"
            zae_response = f"Yess queen! 🔥 {analysis['occasion'] or 'Nail'} vibes - I'm SO here for this!"

            # Ask follow-up question
            if analysis["occasion"]:
                follow_up = f"Tell us more about this {analysis['occasion']} - when is it and what's the vibe you're going for?"
            else:
                follow_up = "What's got you thinking about your nails today? Any special occasion or just treating yourself? 💅"

        else:
            lumi_response = "Hello beautiful! I'm Lumi, and I believe every day is perfect for a little nail magic. ✨"
            zae_response = "Hey there gorgeous! I'm Zae and I'm ready to make your nails absolutely STUNNING! 🔥"
            follow_up = "What brings you to us today? Looking for some nail inspiration or have something specific in mind?"

        return (
            f"🌟 **Lumi**: {lumi_response}\n\n🔥 **Zae**: {zae_response}\n\n{follow_up}"
        )

    def _handle_info_gathering(self, message, analysis, context):
        """Gather information about user needs and preferences"""
        # Store the information they've provided
        if analysis["occasion"]:
            context["occasion"] = analysis["occasion"]
        if analysis["colors_mentioned"]:
            context["preferences"]["colors"] = analysis["colors_mentioned"]
        if analysis["problems_mentioned"]:
            context["gathered_info"]["problems"] = analysis["problems_mentioned"]

        # Generate response based on what they've shared
        if context.get("occasion"):
            lumi_response = f"A {context['occasion']} - how lovely! For such occasions, I always consider the overall aesthetic and lasting power."
            zae_response = f"{context['occasion'].upper()} NAILS! We're gonna make you look absolutely fire! 🔥"

            # Ask about style preference
            follow_up = "Now, are you more drawn to classic elegance or do you want to make a bold statement?"

        elif analysis["problems_mentioned"]:
            lumi_response = "I understand your concerns, dear. Nail health is just as important as beauty."
            zae_response = "Don't worry babe, we've got solutions! Your nails are gonna be stronger than ever!"

            follow_up = "Let's fix this! How long have you been dealing with this issue, and what's your current nail routine?"

        else:
            lumi_response = "I'd love to understand your style better, darling."
            zae_response = "Let's figure out what makes you feel most confident!"

            follow_up = "Are you usually drawn to subtle, natural looks or do you prefer something that makes a statement?"

        return (
            f"🌟 **Lumi**: {lumi_response}\n\n🔥 **Zae**: {zae_response}\n\n{follow_up}"
        )

    def _handle_preference_exploration(self, message, analysis, context):
        """Explore style preferences and narrow down options"""
        # Determine their style preference from their response
        if any(
            word in message.lower()
            for word in ["bold", "statement", "bright", "colorful", "dramatic"]
        ):
            context["preferences"]["style"] = "bold"
            lumi_response = "I admire your confidence, love! Even bold choices can have elegant touches."
            zae_response = "YES! I LOVE the bold energy! We're gonna create something absolutely stunning! 💥"

        elif any(
            word in message.lower()
            for word in ["subtle", "classic", "natural", "simple", "elegant"]
        ):
            context["preferences"]["style"] = "elegant"
            lumi_response = "Exquisite taste, darling! Timeless elegance never goes out of style. ✨"
            zae_response = (
                "Classy vibes! We can definitely make elegant look absolutely bomb! 💎"
            )

        else:
            lumi_response = "I hear you, dear. Let's find the perfect balance for you."
            zae_response = "We'll figure out what makes you feel most YOU! 🌟"

        # Move toward specific design suggestions
        follow_up = "Based on what you've told me, I'm envisioning some amazing options! Would you like to see some specific design ideas, or do you have any colors in mind?"

        return (
            f"🌟 **Lumi**: {lumi_response}\n\n🔥 **Zae**: {zae_response}\n\n{follow_up}"
        )

    def _handle_design_creation(self, message, analysis, context):
        """Create specific design recommendations"""
        style = context["preferences"].get("style", "balanced")
        context.get("occasion", "general")

        # Generate specific designs based on their preferences
        if style == "bold":
            lumi_design = "For you, darling, I'm thinking rich burgundy with gold accent details - bold yet sophisticated."
            zae_design = "How about holographic chrome with geometric patterns?! It's gonna be EVERYTHING! ✨"
        else:
            lumi_design = "I envision soft champagne with subtle pearl accents - timeless and refined."
            zae_design = "What about a gorgeous nude with delicate rose gold details? Classy but with that special sparkle! 💫"

        follow_up = "Which direction speaks to you more? We can always adjust the colors or add special touches!"

        return f"🌟 **Lumi suggests**: {lumi_design}\n\n🔥 **Zae suggests**: {zae_design}\n\n{follow_up}"

    def _handle_design_refinement(self, message, analysis, context):
        """Refine the chosen design based on feedback"""
        lumi_response = "Perfect choice, love! Let's make sure every detail is exactly right for you."
        zae_response = (
            "Yes! Now we're cooking! Let's make this design absolutely perfect! 🔥"
        )

        follow_up = "Any specific adjustments you'd like? Different colors, finishes, or special details?"

        return (
            f"🌟 **Lumi**: {lumi_response}\n\n🔥 **Zae**: {zae_response}\n\n{follow_up}"
        )

    def _handle_general_conversation(self, message, analysis, context):
        """Handle general conversation while maintaining personality"""
        if not analysis["contains_nail_terms"]:
            # Acknowledge their message but steer back naturally
            lumi_response = "That's interesting, darling! You know what would complement that perfectly?"
            zae_response = "I hear you, babe! But can we talk about something that'll make you feel even MORE amazing?"
            follow_up = "Your nails! When's the last time you treated yourself to something special? 💅"
        else:
            # Continue nail conversation
            lumi_response = "I love discussing nail artistry, dear!"
            zae_response = "Nail talk is my FAVORITE topic! 🔥"
            follow_up = "What specifically would you like to know more about?"

        return (
            f"🌟 **Lumi**: {lumi_response}\n\n🔥 **Zae**: {zae_response}\n\n{follow_up}"
        )

    def _update_conversation_state(self, analysis, context, user_id):
        """Update conversation state based on the interaction"""
        context["question_count"] += 1

        # Progress through conversation stages
        if context["stage"] == "initial" and (
            analysis["contains_nail_terms"] or analysis["occasion"]
        ):
            context["stage"] = "gathering_basic_info"
        elif (
            context["stage"] == "gathering_basic_info"
            and context["question_count"] >= 2
        ):
            context["stage"] = "exploring_preferences"
        elif context["stage"] == "exploring_preferences" and context.get("preferences"):
            context["stage"] = "design_creation"
        elif context["stage"] == "design_creation" and context["question_count"] >= 5:
            context["stage"] = "refinement"


# Create global instance
nail_personalities = NailPersonalities()
