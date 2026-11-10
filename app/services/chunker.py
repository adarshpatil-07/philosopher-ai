from app.config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_pages(pages: list[dict], book_title: str) -> list[dict]:
    """Split page text into overlapping chunks, keeping book + page metadata."""
    chunks = []
    for p in pages:
        text = " ".join(p["text"].split())  # collapse whitespace and newlines
        start = 0
        while start < len(text):
            end = start + CHUNK_SIZE
            chunks.append({
                "text": text[start:end],
                "book": book_title,
                "page": p["page"],
            })
            if end >= len(text):
                break
            start = end - CHUNK_OVERLAP
    return chunks