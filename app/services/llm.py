import time
from google import genai
from google.genai import types
from google.genai.errors import APIError, ClientError, ServerError
from app.config import GEMINI_API_KEY

_client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(timeout=30_000),
)

MODELS = ["gemini-3.1-flash-lite", "gemini-3.8-flash"]
RETRIES = 3


def generate(system_prompt: str, history: list[dict], message: str) -> str:
    contents = []

    for h in history:
        role = "user" if h["role"] == "user" else "model"
        contents.append(
            types.Content(
                role=role,
                parts=[types.Part(text=h["content"])]
            )
        )

    contents.append(
        types.Content(
            role="user",
            parts=[types.Part(text=message)]
        )
    )

    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=0.8,
    )

    last_error = None

    for model in MODELS:
        for attempt in range(RETRIES):
            try:
                response = _client.models.generate_content(
                    model=model,
                    contents=contents,
                    config=config,
                )

                if response.text is None:
                    raise ValueError("Gemini returned an empty response")

                return response.text

            except (ServerError, ClientError, APIError, ValueError) as e:
                last_error = e
                if attempt < RETRIES - 1:
                    time.sleep(2 ** attempt)
                else:
                    break

    if last_error is not None:
        raise last_error

    raise RuntimeError("Gemini request failed without returning a response")