# test_key.py
import os
from dotenv import load_dotenv
import openai

# 1. Load your .env
load_dotenv()

# 2. Set the API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# 3. Try a simple chat completion with the new interface
try:
    resp = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user",   "content": "Ping"}
        ]
    )
    print("✅ Key works! Here’s the model’s reply:")
    print(resp.choices[0].message.content)
except Exception as e:
    print("❌ API call failed:", e)