import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TwiNailzAI:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY')
        )
    
    def get_nail_recommendation(self, user_prompt):
        """Get AI-powered nail recommendations"""
        try:
            completion = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are TwiNailz AI, an expert nail artist and trend advisor. Provide creative, trendy nail design recommendations, color suggestions, and nail care tips. Keep responses engaging and fashionable."
                    },
                    {
                        "role": "user", 
                        "content": user_prompt
                    }
                ]
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Sorry, I couldn't process your request: {str(e)}"
    
    def get_nail_trends(self):
        """Get current nail trends"""
        try:
            completion = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are TwiNailz AI. Provide the latest nail trends, popular colors, and seasonal nail designs. Be specific and trendy."
                    },
                    {
                        "role": "user",
                        "content": "What are the current nail trends and popular designs right now?"
                    }
                ]
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Sorry, I couldn't get trends: {str(e)}"