import BookManager from "./BookManager";
import { useEffect, useRef, useState } from "react";
import { sendChat } from "../api";

export default function Chat({ persona, onBack }) {
  const [messages, setMessages] = useState([]);
  const [showBooks, setShowBooks] = useState(false);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [showSources, setShowSources] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function handleSend(e) {
    e.preventDefault();
    const text = input.trim();
    if (!text || loading) return;

    const history = messages
      .filter((m) => !m.error)
      .map(({ role, content }) => ({ role, content }));

    setMessages((prev) => [...prev, { role: "user", content: text }]);
    setInput("");
    setLoading(true);

    try {
      const data = await sendChat({
        persona: persona.id,
        message: text,
        history,
        showSources,
      });
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.reply, sources: data.sources },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: err.message, error: true },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="chat">
      <header className="chat-header">
        <button className="back" onClick={onBack}>
          ← Back
        </button>
        <h2>{persona.name}</h2>
        <button className="back" onClick={() => setShowBooks((s) => !s)}>
  Books
</button>
        <label className="toggle">
          <input
            type="checkbox"
            checked={showSources}
            onChange={(e) => setShowSources(e.target.checked)}
          />
          Show sources
        </label>
      </header>
      {showBooks && <BookManager persona={persona} />}

      <div className="messages">
        {messages.length === 0 && (
          <p className="hint">Ask {persona.name} anything about his work.</p>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`bubble ${m.role} ${m.error ? "error" : ""}`}>
            <p>{m.content}</p>
            {m.sources?.length > 0 && (
              <details>
                <summary>Sources ({m.sources.length})</summary>
                {m.sources.map((s, j) => (
                  <blockquote key={j}>
                    <strong>
                      {s.book}, p.{s.page}
                    </strong>
                    <br />
                    {s.text}
                  </blockquote>
                ))}
              </details>
            )}
          </div>
        ))}
        {loading && <div className="bubble assistant">Thinking…</div>}
        <div ref={bottomRef} />
      </div>

      <form className="input-row" onSubmit={handleSend}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={`Message ${persona.name}…`}
        />
        <button type="submit" disabled={loading || !input.trim()}>
          Send
        </button>
      </form>
    </div>
  );
}