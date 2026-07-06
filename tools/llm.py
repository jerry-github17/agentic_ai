import time
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
print("KEY PREFIX:", os.getenv("GEMINI_API_KEY")[:10])

client=genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def call_llm(prompt: str):

    #retry-fallback logic
    retries = 3
    delay=10
    for i in range(retries):
        try: 
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
                )
            return response.text.strip()
        except Exception as e:
            if "429" in str(e) or "Resource_Exhausted" in str(e):
                wait = delay *(i+1)
                print(f"Rate Limit hit. Retrying in {wait} seconds....")
                time.sleep(wait)
            else:
                raise
        raise Exception("Gemini quota exhausted after retries")        