import { useState } from "react";
import "./App.css";

function App() {
  const [id, setId] = useState("");
  const [type, setType] = useState("item");
  const [results, setResults] = useState<{
    collaborative: number[];
    content: number[];
    wideAndDeep: number[];
  } | null>(null);

  const handleSubmit = async () => {
    const response = await fetch("https://localhost:5000/api/recommendations", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id, type }),
    });

    const data = await response.json();
    setResults(data);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h2>Recommendation System</h2>

      <div style={{ marginBottom: "1rem" }}>
        <label>Enter User or Item ID:</label>
        <br />
        <input
          type="text"
          value={id}
          onChange={(e) => setId(e.target.value)}
          style={{ width: "300px" }}
        />
      </div>

      <div style={{ marginBottom: "1rem" }}>
        <label>Select Type:</label>
        <br />
        <select value={type} onChange={(e) => setType(e.target.value)}>
          <option value="user">User</option>
          <option value="item">Item</option>
        </select>
      </div>

      <button onClick={handleSubmit}>Get Recommendations</button>

      {results && (
        <div style={{ marginTop: "2rem" }}>
          <h3>Collaborative</h3>
          <ul>
            {results.collaborative.map((id) => (
              <li key={id}>{id}</li>
            ))}
          </ul>

          <h3>Content-Based</h3>
          <ul>
            {results.content.map((id) => (
              <li key={id}>{id}</li>
            ))}
          </ul>

          <h3>Wide and Deep (Azure ML)</h3>
          <ul>
            {results.wideAndDeep.map((id) => (
              <li key={id}>{id}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
