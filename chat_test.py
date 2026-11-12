import sys
from app.personas.registry import PERSONAS
from app.personas.base import build_system_prompt
from app.services.vector_store import search
from app.services.llm import generate

persona_id = sys.argv[1] if len(sys.argv) > 1 else "kafka"
if persona_id not in PERSONAS:
    print("Unknown persona. Choose from:", ", ".join(PERSONAS))
    sys.exit(1)

PERSONA = PERSONAS[persona_id]
history = []
print(f"Chat with {PERSONA['name']} (type 'exit' to quit)")

while True:
    q = input("\nYou: ").strip()
    if q.lower() in ("exit", "quit"):
        break

    passages = search(PERSONA["id"], q, k=4)
    system_prompt = build_system_prompt(PERSONA, passages)
    answer = generate(system_prompt, history[-6:], q)

    history.append({"role": "user", "content": q})
    history.append({"role": "assistant", "content": answer})
    print(f"\n{PERSONA['name']}:", answer)