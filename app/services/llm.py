import time
from google import genai
from google.genai import types
from google.genai.errors import ServerError
from app.config import GEMINI_API_KEY

_client = genai.Client(api_key=GEMINI_API_KEY)

MODELS = ["gemini-3.8-flash", "gemini-3.8-flash-lite"]  # tried in order
RETRIES = 3


def generate(system_prompt: str, history: list[dict], message: str) -> str:
    contents = []
    for h in history:
        role = "user" if h["role"] == "user" else "model"
        contents.append(
            types.Content(role=role, parts=[types.Part(text=h["content"])])
        )
    contents.append(types.Content(role="user", parts=[types.Part(text=message)]))

    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=0.8,
    )

    last_error = None
    for model in MODELS:
        for attempt in range(RETRIES):
            try:
                response = _client.models.generate_content(
                    model=model, contents=contents, config=config
                )
                return response.text
            except ServerError as e:
                last_error = e
                time.sleep(2 ** attempt)  # waits 1s, 2s, 4s

    raise last_error