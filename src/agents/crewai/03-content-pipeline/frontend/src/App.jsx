import { useState } from 'react'
import ReactMarkdown from 'react-markdown'

const STAGES = ['Research', 'Writing', 'QA Review', 'Published']

function App() {
  const [form, setForm] = useState({
    topic: '',
    target_audience: 'tech professionals',
    content_type: 'blog post',
    tone: 'professional yet approachable',
    word_count: 800,
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleChange = (field, value) => {
    setForm((prev) => ({ ...prev, [field]: value }))
  }

  const handleSubmit = async () => {
    if (!form.topic.trim()) return
    setLoading(true)
    setError('')
    setResult(null)
    try {
      const res = await fetch('/create-content', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      })
      if (!res.ok) throw new Error(`Request failed: ${res.status}`)
      const data = await res.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const activeStage = loading ? 1 : result ? 3 : -1

  return (
    <div className="app">
      <header className="header">
        <h1>Content Marketing Pipeline</h1>
        <p>Inspired by Jasper AI — multi-crew content creation with quality gates</p>
      </header>
      <main className="main">
        <div className="brief-form">
          <h2>Content Brief</h2>
          <div className="form-grid">
            <div className="form-group full">
              <label>Topic</label>
              <input
                type="text"
                value={form.topic}
                onChange={(e) => handleChange('topic', e.target.value)}
                placeholder="e.g., The Future of AI Agents in Enterprise"
                className="text-input"
              />
            </div>
            <div className="form-group">
              <label>Content Type</label>
              <select value={form.content_type} onChange={(e) => handleChange('content_type', e.target.value)} className="select-input">
                <option value="blog post">Blog Post</option>
                <option value="article">Article</option>
                <option value="tutorial">Tutorial</option>
                <option value="newsletter">Newsletter</option>
              </select>
            </div>
            <div className="form-group">
              <label>Target Audience</label>
              <input type="text" value={form.target_audience} onChange={(e) => handleChange('target_audience', e.target.value)} className="text-input" />
            </div>
            <div className="form-group">
              <label>Tone</label>
              <input type="text" value={form.tone} onChange={(e) => handleChange('tone', e.target.value)} className="text-input" />
            </div>
            <div className="form-group">
              <label>Word Count: {form.word_count}</label>
              <input type="range" min={300} max={2000} step={100} value={form.word_count} onChange={(e) => handleChange('word_count', parseInt(e.target.value))} className="range-input" />
            </div>
          </div>
          <button onClick={handleSubmit} disabled={loading || !form.topic.trim()} className="submit-btn">
            {loading ? 'Creating Content...' : 'Create Content'}
          </button>
        </div>

        <div className="pipeline">
          {STAGES.map((stage, i) => (
            <div key={stage} className={`pipeline-stage ${i <= activeStage ? 'active' : ''} ${i === activeStage ? 'current' : ''}`}>
              <div className="stage-dot" />
              <span>{stage}</span>
            </div>
          ))}
        </div>

        {error && <div className="error-banner">{error}</div>}

        {loading && (
          <div className="loading">
            <div className="loading-spinner" />
            <p>Running the content pipeline... This may take a few minutes.</p>
          </div>
        )}

        {result && (
          <div className="result-card">
            <div className="result-meta">
              <div className="quality-score">
                <svg viewBox="0 0 36 36" className="score-ring">
                  <path d="M18 2.0845a 15.9155 15.9155 0 0 1 0 31.831a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#e2e8f0" strokeWidth="3" />
                  <path d="M18 2.0845a 15.9155 15.9155 0 0 1 0 31.831a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke={result.quality_score >= 75 ? '#7c3aed' : '#d97706'} strokeWidth="3" strokeDasharray={`${result.quality_score}, 100`} />
                </svg>
                <span className="score-text">{result.quality_score}</span>
              </div>
              <div className="meta-info">
                <span className="status-badge">{result.status}</span>
                <span className="revision-badge">{result.revision_count} revision{result.revision_count !== 1 ? 's' : ''}</span>
              </div>
            </div>
            <div className="content-output">
              <ReactMarkdown>{result.content}</ReactMarkdown>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
