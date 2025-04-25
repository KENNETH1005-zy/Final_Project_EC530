import os, json
import openai
from dotenv import load_dotenv

# Load environment variables (needs .env with OPENAI_API_KEY)
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_document(text: str) -> dict:
    """
    Send `text` to the LLM and return a dict containing:
      - summary
      - key_points
      - quiz
      - feedback
      - grade
    """
    prompt = (
        "You are a Document Analyzer for teachers. "
        "Given the following document text, generate teaching materials "
        "(summary, key points, quiz questions), provide feedback suggestions, "
        "and assign a grade from A to F.\n\n"
        f"Document Text:\n{text}\n\n"
        "Output as JSON with fields: summary, key_points, quiz, feedback, grade."
    )

    # v1 API call
    resp = openai.chat.completions.create(
        model="gpt-3.5-turbo",       # or use "gpt-4o-mini" if available
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024
    )

    return json.loads(resp.choices[0].message.content)