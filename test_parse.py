from app.services.pdf_parser import extract_pages
from app.services.chunker import chunk_pages

pages = extract_pages("data/uploads/the-metamorphosis.pdf")
chunks = chunk_pages(pages, "the-metamorphosis")

print(len(pages), "pages ->", len(chunks), "chunks")
print(chunks[5])