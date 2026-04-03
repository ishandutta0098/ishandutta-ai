import { useState } from 'react'
import ReactMarkdown from 'react-markdown'

function App() {
  const [topic, setTopic] = useState('')
  const [newsletter, setNewsletter] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleGenerate = async () => {
    if (!topic.trim()) return
    setLoading(true)
    setError('')
    setNewsletter('')
    try {
      const res = await fetch('/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic, num_stories: 5 }),
      })
      if (!res.ok) throw new Error(`Request failed: ${res.status}`)
      const data = await res.json()
      setNewsletter(data.newsletter)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>TLDR Newsletter Generator</h1>
        <p>Inspired by tldr.tech — AI-powered tech news digest</p>
      </header>
      <main className="main">
        <div className="input-section">
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="e.g., AI Agents, Quantum Computing, Web3"
            className="topic-input"
            onKeyDown={(e) => e.key === 'Enter' && handleGenerate()}
          />
          <button
            onClick={handleGenerate}
            disabled={loading || !topic.trim()}
            className="generate-btn"
          >
            {loading ? 'Generating...' : 'Generate Newsletter'}
          </button>
        </div>
        {error && <div className="error-banner">{error}</div>}
        {loading && (
          <div className="loading">
            <div className="loading-pulse" />
            <p>Generating your newsletter... This may take a minute.</p>
          </div>
        )}
        {newsletter && (
          <div className="newsletter-card">
            <ReactMarkdown>{newsletter}</ReactMarkdown>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
