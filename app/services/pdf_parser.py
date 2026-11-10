from pypdf import PdfReader


def extract_pages(path: str) -> list[dict]:
    """Return a list of {"page": int, "text": str} for every page with text."""
    reader = PdfReader(path)
    pages = []
    for i, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if text:
            pages.append({"page": i, "text": text})

    if not pages:
        raise ValueError("No text found. This PDF may be scanned images (needs OCR).")
    return pages