from fastapi import APIRouter, HTTPException
from app.schemas import ChatRequest, ChatResponse
from app.personas.registry import PERSONAS
from app.personas.base import build_system_prompt
from app.services.vector_store import search
from app.services.llm import generate

router = APIRouter()


@router.get("/personas")
def list_personas():
    return [{"id": p["id"], "name": p["name"]} for p in PERSONAS.values()]


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    persona = PERSONAS.get(req.persona)
    if not persona:
        raise HTTPException(404, "Unknown persona")

    passages = search(persona["id"], req.message, k=4)
    system_prompt = build_system_prompt(persona, passages)
    history = [h.model_dump() for h in req.history[-6:]]

    try:
        reply = generate(system_prompt, history, req.message)
    except Exception:
        raise HTTPException(503, "The model is busy. Please try again.")

    return ChatResponse(
        persona=persona["id"],
        reply=reply,
        sources=passages if req.show_sources else [],
    )