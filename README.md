# Philosopher AI

Chat with **Franz Kafka**, **Fyodor Dostoevsky**, or **Marcus Aurelius** in their own voice, grounded in the books you upload.



## What it does

- Pick a writer and talk to them in the first person
- Upload your own PDFs of their books; answers draw on those texts
- Optional "Show sources" toggle reveals the exact passages behind a reply
- Replies stay in character and avoid quoting in every answer

## How it works

This is **RAG** (retrieval-augmented generation), not model training:

1. Your PDF is split into overlapping chunks, each tagged with book and page
2. Chunks are embedded locally with `all-MiniLM-L6-v2` and stored in ChromaDB (one collection per persona)
3. When you ask a question, the most relevant chunks are retrieved
4. The chunks and a persona prompt go to Gemini, which answers as that writer

## Tech stack

- **Backend:** FastAPI, ChromaDB, sentence-transformers, pypdf
- **LLM:** Google Gemini API
- **Frontend:** React + Vite

## Project structure

```
philosopher-ai/
├── app/                        # FastAPI backend
│   ├── main.py                 # App setup, CORS, routers
│   ├── config.py               # Env vars, paths, chunking settings
│   ├── schemas.py              # Request/response models
│   ├── routers/
│   │   ├── chat.py             # /personas and /chat
│   │   └── books.py            # Upload, list, delete books
│   ├── services/
│   │   ├── pdf_parser.py       # Extract text from PDFs
│   │   ├── chunker.py          # Split text into overlapping chunks
│   │   ├── vector_store.py     # ChromaDB: embed, store, search
│   │   └── llm.py              # Gemini call with retry and fallback
│   └── personas/
│       ├── base.py             # Shared system prompt template
│       ├── registry.py         # Maps persona ids to persona configs
│       ├── kafka.py
│       ├── dostoevsky.py
│       └── marcus.py
├── frontend/                   # React + Vite app
│   └── src/
│       ├── App.jsx
│       ├── api.js              # Backend calls
│       └── components/
│           ├── PersonaPicker.jsx
│           ├── Chat.jsx
│           └── BookManager.jsx
├── docs/                       # README screenshots
├── ingest.py                   # CLI: load a PDF into a persona
├── chat_test.py                # CLI: chat with a persona in the terminal
├── requirements.txt
├── .env.example
└── LICENSE
```

`data/` (uploaded PDFs and the vector database) is created at runtime and is gitignored.

## Run it locally

You need Python 3.11+, Node 20+, and a free [Gemini API key](https://aistudio.google.com).

```bash
# Backend (from the project root)
python -m venv venv
venv\Scripts\activate        # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env         # then add your GEMINI_API_KEY
uvicorn app.main:app --reload
```

```bash
# Frontend (in a second terminal)
cd frontend
cp .env.example .env
npm install
npm run dev
```

Open http://localhost:5173, choose a writer, click **Books**, and upload a PDF.

You can also load a book from the command line and chat in the terminal:

```bash
python ingest.py kafka "The Metamorphosis" path/to/book.pdf
python chat_test.py kafka
```

## API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/personas` | List available writers |
| POST | `/chat` | Send a message, get an in-character reply |
| GET | `/books?persona=` | List uploaded books |
| POST | `/books/upload` | Upload and index a PDF |
| DELETE | `/books` | Remove a book |

Interactive docs are at http://127.0.0.1:8000/docs.

## Notes

- No books are included. You upload your own PDFs, so nothing copyrighted lives in this repo.
- Scanned (image-only) PDFs are not supported yet; the PDF needs selectable text.
- Replies are AI interpretations in the style of each writer, not their actual words.

## Roadmap

- Similarity cutoff to drop weak matches
- Per-user book storage
- Deployment
- More personas

## Credits

- Writers: Franz Kafka, Fyodor Dostoevsky, and Marcus Aurelius. The personas are AI interpretations of their voices, not their actual words.
- Texts: you supply your own PDFs. Original works by these authors are public domain, but some translations and editions are still under copyright, so check the edition you upload.
- [Google Gemini](https://ai.google.dev) for language generation
- [ChromaDB](https://www.trychroma.com) for vector storage
- [sentence-transformers](https://www.sbert.net) and the `all-MiniLM-L6-v2` model for embeddings
- [FastAPI](https://fastapi.tiangolo.com), [React](https://react.dev), and [Vite](https://vite.dev)
- [pypdf](https://pypdf.readthedocs.io) for PDF text extraction

## License

Released under the [MIT License](LICENSE). The license covers this project's code only, not the books you upload or any third-party libraries, which keep their own licenses.