from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    persona: str
    message: str
    history: list[ChatMessage] = []
    show_sources: bool = False


class Source(BaseModel):
    book: str
    page: int
    text: str


class ChatResponse(BaseModel):
    persona: str
    reply: str
    sources: list[Source] = []