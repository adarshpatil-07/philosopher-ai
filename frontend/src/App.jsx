import { useEffect, useState } from "react";
import { getPersonas } from "./api";
import PersonaPicker from "./components/PersonaPicker";
import Chat from "./components/Chat ";

export default function App() {
  const [personas, setPersonas] = useState([]);
  const [selected, setSelected] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getPersonas()
      .then(setPersonas)
      .catch(() => setError("Cannot reach the backend. Is uvicorn running?"));
  }, []);

  if (error) return <p className="error-msg">{error}</p>;

  return selected ? (
    <Chat key={selected.id} persona={selected} onBack={() => setSelected(null)} />
  ) : (
    <PersonaPicker personas={personas} onSelect={setSelected} />
  );
}