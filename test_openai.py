import os
import openai

client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

try:
    models = client.models.list()
    print("API key works! Models:", [m.id for m in models.data])
except Exception as e:
    print("Error:", e)