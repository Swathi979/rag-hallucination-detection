import React, { useState } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleQuery = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${process.env.REACT_APP_API_URL}/api/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query_text: query, top_k: 5 })
      });
      const data = await res.json();
      setResponse(data);
    } catch (error) {
      console.error('Error:', error);
    }
    setLoading(false);
  };

  return (
    <div className="App" style={{ padding: '20px' }}>
      <h1>RAG Hallucination Detection</h1>
      <textarea
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter your query..."
        style={{ width: '100%', height: '100px', marginBottom: '10px' }}
      />
      <button onClick={handleQuery} disabled={loading} style={{ padding: '10px 20px' }}>
        {loading ? 'Processing...' : 'Ask'}
      </button>
      {response && (
        <div style={{ marginTop: '20px', border: '1px solid #ccc', padding: '10px' }}>
          <h3>Answer:</h3>
          <p>{response.answer}</p>
          <p>Trust Score: {response.trust_score?.toFixed(1) || 'N/A'}</p>
          <p>Risk Level: {response.risk_level || 'N/A'}</p>
        </div>
      )}
    </div>
  );
}

export default App;
