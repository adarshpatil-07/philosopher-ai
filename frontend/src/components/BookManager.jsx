import { useEffect, useState } from "react";
import { listBooks, uploadBook, deleteBook } from "../api";

export default function BookManager({ persona }) {
  const [books, setBooks] = useState([]);
  const [title, setTitle] = useState("");
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");
  const [busy, setBusy] = useState(false);

  async function refresh() {
    try {
      const data = await listBooks(persona.id);
      setBooks(data.books);
    } catch (err) {
      setStatus(err.message);
    }
  }

  useEffect(() => {
    refresh();
  }, [persona.id]);

  async function handleUpload(e) {
    e.preventDefault();
    if (!file || !title.trim() || busy) return;
    setBusy(true);
    setStatus("Processing the book. Large books can take a few minutes…");
    try {
      const res = await uploadBook({ persona: persona.id, title: title.trim(), file });
      setStatus(`Added "${res.book}" (${res.chunks} passages).`);
      setTitle("");
      setFile(null);
      e.target.reset();
      await refresh();
    } catch (err) {
      setStatus(err.message);
    } finally {
      setBusy(false);
    }
  }

  async function handleDelete(bookTitle) {
    if (!window.confirm(`Remove "${bookTitle}"?`)) return;
    try {
      await deleteBook(persona.id, bookTitle);
      await refresh();
    } catch (err) {
      setStatus(err.message);
    }
  }

  return (
    <div className="books-panel">
      <h3>Books for {persona.name}</h3>

      {books.length === 0 ? (
        <p className="hint-small">No books yet. Upload a PDF below.</p>
      ) : (
        <ul>
          {books.map((b) => (
            <li key={b}>
              {b}
              <button onClick={() => handleDelete(b)}>Remove</button>
            </li>
          ))}
        </ul>
      )}

      <form onSubmit={handleUpload}>
        <input
          placeholder="Book title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files[0] || null)}
        />
        <button type="submit" disabled={busy || !file || !title.trim()}>
          {busy ? "Processing…" : "Upload"}
        </button>
      </form>

      {status && <p className="hint-small">{status}</p>}
    </div>
  );
}