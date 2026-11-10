from app.personas.kafka import PERSONA
from app.personas.base import build_system_prompt
from app.services.vector_store import search
from app.services.llm import generate

history = []
print("Chat with Kafka (type 'exit' to quit)")

while True:
    q = input("\nYou: ").strip()
    if q.lower() in ("exit", "quit"):
        break

    print("searching books...")
    passages = search(PERSONA["id"], q, k=4)
    print(f"found {len(passages)} passages, calling Gemini...")
    system_prompt = build_system_prompt(PERSONA, passages)
    answer = generate(system_prompt, history[-6:], q)

    history.append({"role": "user", "content": q})
    history.append({"role": "assistant", "content": answer})
    print("\nKafka:", answer)