const TAGLINES = {
  kafka: "Guilt, bureaucracy, and the absurd",
  dostoevsky: "Suffering, doubt, and the lonely dreamer",
  marcus: "Duty, discipline, and what is in your control",
};

export default function PersonaPicker({ personas, onSelect }) {
  return (
    <div className="picker">
      <h1>Philosopher AI</h1>
      <p className="subtitle">Choose who you want to talk to.</p>
      <div className="cards">
        {personas.map((p) => (
          <button key={p.id} className="card" onClick={() => onSelect(p)}>
            <h2>{p.name}</h2>
            <p>{TAGLINES[p.id] || ""}</p>
          </button>
        ))}
      </div>
    </div>
  );
}