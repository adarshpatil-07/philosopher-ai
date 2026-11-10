from app.services.pdf_parser import extract_pages
from app.services.chunker import chunk_pages
from app.services.vector_store import add_chunks, search, delete_book

PERSONA = "kafka"
BOOK = "The Metamorphosis"

delete_book(PERSONA, BOOK)  # avoids duplicates when you re-run this test
pages = extract_pages("data/uploads/metamorphosis.pdf")
n = add_chunks(PERSONA, chunk_pages(pages, BOOK))
print("Stored", n, "chunks")

questions = [
    "How did Gregor's family react when they saw him as an insect?",
    "Why does Gregor worry about his job?",
    "What happens to Gregor at the end?",
]

for q in questions:
    print("\nQ:", q)
    for r in search(PERSONA, q, k=3):
        print(f"  [{r['book']} p.{r['page']}] {r['text'][:150]}...")