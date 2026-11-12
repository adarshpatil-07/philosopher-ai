from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import books, chat

app = FastAPI(title="Philosopher AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(books.router)


@app.get("/")
def root():
    return {"status": "ok"}