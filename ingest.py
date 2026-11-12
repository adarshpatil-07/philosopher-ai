import sys
from app.services.pdf_parser import extract_pages
from app.services.chunker import chunk_pages
from app.services.vector_store import add_chunks, delete_book

if len(sys.argv) != 4:
    print('Usage: python ingest.py <persona> "<Book Title>" <pdf_path>')
    sys.exit(1)

persona, title, path = sys.argv[1], sys.argv[2], sys.argv[3]

delete_book(persona, title)  # avoids duplicates on re-run
pages = extract_pages(path)
n = add_chunks(persona, chunk_pages(pages, title))
print(f"Stored {n} chunks for {persona}: {title}")