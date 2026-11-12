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