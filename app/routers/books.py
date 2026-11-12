import os
import shutil
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.config import UPLOAD_DIR
from app.personas.registry import PERSONAS
from app.services.pdf_parser import extract_pages
from app.services.chunker import chunk_pages
from app.services.vector_store import add_chunks, list_books, delete_book

router = APIRouter(prefix="/books")


def _check(persona: str):
    if persona not in PERSONAS:
        raise HTTPException(404, "Unknown persona")


@router.get("")
def books(persona: str):
    _check(persona)
    return {"persona": persona, "books": list_books(persona)}


@router.post("/upload")
def upload(
    persona: str = Form(...),
    title: str = Form(...),
    file: UploadFile = File(...),
):
    _check(persona)
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are supported")

    path = os.path.join(UPLOAD_DIR, f"{persona}_{os.path.basename(file.filename)}")
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        pages = extract_pages(path)
    except ValueError as e:
        raise HTTPException(422, str(e))

    delete_book(persona, title)
    n = add_chunks(persona, chunk_pages(pages, title))
    return {"persona": persona, "book": title, "chunks": n}


@router.delete("")
def remove(persona: str, title: str):
    _check(persona)
    delete_book(persona, title)
    return {"deleted": title}