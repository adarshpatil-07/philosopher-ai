const API = import.meta.env.VITE_API_URL;

export async function getPersonas() {
  const res = await fetch(`${API}/personas`);
  if (!res.ok) throw new Error("Cannot load personas");
  return res.json();
}

export async function sendChat({ persona, message, history, showSources }) {
  const res = await fetch(`${API}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      persona,
      message,
      history,
      show_sources: showSources,
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Something went wrong. Try again.");
  }
  return res.json();
}

export async function listBooks(persona) {
  const res = await fetch(`${API}/books?persona=${encodeURIComponent(persona)}`);
  if (!res.ok) throw new Error("Cannot load books");
  return res.json();
}

export async function uploadBook({ persona, title, file }) {
  const form = new FormData();
  form.append("persona", persona);
  form.append("title", title);
  form.append("file", file);
  const res = await fetch(`${API}/books/upload`, { method: "POST", body: form });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Upload failed");
  }
  return res.json();
}

export async function deleteBook(persona, title) {
  const res = await fetch(
    `${API}/books?persona=${encodeURIComponent(persona)}&title=${encodeURIComponent(title)}`,
    { method: "DELETE" }
  );
  if (!res.ok) throw new Error("Could not delete book");
  return res.json();
}