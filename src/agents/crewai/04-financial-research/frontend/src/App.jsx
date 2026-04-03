import { useState, useRef, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'

function RatingBadge({ rating }) {
  const colors = {
    Buy: { bg: '#059669', text: '#ffffff' },
    Hold: { bg: '#d97706', text: '#ffffff' },
    Sell: { bg: '#dc2626', text: '#ffffff' },
  }
  const style = colors[rating] || colors.Hold
  return (
    <span className="rating-badge" style={{ backgroundColor: style.bg, color: style.text }}>
      {rating}
    </span>
  )
}

function ExecutionLog({ logs, isOpen, onToggle }) {
  const logEndRef = useRef(null)

  useEffect(() => {
    if (isOpen && logEndRef.current) {
      logEndRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [logs, isOpen])

  return (
    <div className="execution-log">
      <button className="log-toggle" onClick={onToggle}>
        <span className="log-toggle-icon">{isOpen ? '▼' : '▶'}</span>
        Execution Log ({logs.length} entries)
      </button>
      {isOpen && (
        <div className="log-viewer">
          {logs.length === 0 ? (
            <div className="log-empty">No log entries yet...</div>
          ) : (
            logs.map((entry, i) => (
              <div key={i} className="log-entry">{entry}</div>
            ))
          )}
          <div ref={logEndRef} />
        </div>
      )}
    </div>
  )
}

export default function App() {
  const [company, setCompany] = useState('')
  const [ticker, setTicker] = useState('')
  const [loading, setLoading] = useState(false)
  const [report, setReport] = useState(null)
  const [error, setError] = useState('')
  const [logOpen, setLogOpen] = useState(false)
  const [liveLog, setLiveLog] = useState([])
  const pollRef = useRef(null)

  const pollLogs = () => {
    pollRef.current = setInterval(async () => {
      const res = await fetch('/logs')
      if (res.ok) {
        const data = await res.json()
        setLiveLog(data.logs || [])
      }
    }, 2000)
  }

  const stopPolling = () => {
    if (pollRef.current) {
      clearInterval(pollRef.current)
      pollRef.current = null
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!company.trim()) return

    setLoading(true)
    setError('')
    setReport(null)
    setLiveLog([])
    setLogOpen(true)
    pollLogs()

    const res = await fetch('/research', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ company: company.trim(), ticker: ticker.trim() }),
    })

    stopPolling()

    if (!res.ok) {
      setError(`Request failed with status ${res.status}`)
      setLoading(false)
      return
    }

    const data = await res.json()
    setReport(data)
    setLiveLog(data.execution_log || [])
    setLoading(false)
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <div className="header-icon">
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
              <rect width="32" height="32" rx="8" fill="#059669" />
              <path d="M8 22V10h10v3H11.5v2H17v3h-5.5v4H8z" fill="white" />
              <path d="M20 10h3.5v12H20V10z" fill="white" />
            </svg>
          </div>
          <div>
            <h1>Financial Research Report Generator</h1>
            <p className="subtitle">Inspired by Finchat.io &mdash; AI-powered equity research</p>
          </div>
        </div>
      </header>

      <main className="main">
        <form className="search-form" onSubmit={handleSubmit}>
          <div className="search-bar">
            <div className="search-icon">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="8.5" cy="8.5" r="5.5" />
                <path d="M12.5 12.5L17 17" />
              </svg>
            </div>
            <input
              type="text"
              className="input-company"
              placeholder="Company name (e.g., Apple, Tesla, Microsoft)"
              value={company}
              onChange={(e) => setCompany(e.target.value)}
              disabled={loading}
            />
            <input
              type="text"
              className="input-ticker"
              placeholder="Ticker (optional)"
              value={ticker}
              onChange={(e) => setTicker(e.target.value)}
              disabled={loading}
            />
            <button type="submit" className="btn-generate" disabled={loading || !company.trim()}>
              {loading ? (
                <span className="spinner" />
              ) : (
                'Generate Report'
              )}
            </button>
          </div>
        </form>

        {loading && (
          <div className="loading-section">
            <div className="loading-bar">
              <div className="loading-bar-fill" />
            </div>
            <p className="loading-text">
              Agents are researching <strong>{company}</strong>... This may take a few minutes.
            </p>
            <ExecutionLog logs={liveLog} isOpen={logOpen} onToggle={() => setLogOpen(!logOpen)} />
          </div>
        )}

        {error && (
          <div className="error-card">
            <p>{error}</p>
          </div>
        )}

        {report && (
          <div className="report-section">
            <div className="report-header-card">
              <div className="report-header-top">
                <div>
                  <h2 className="report-company">{report.company}</h2>
                  <span className="report-ticker">{report.ticker}</span>
                </div>
                <RatingBadge rating={report.rating} />
              </div>
              <p className="report-meta">
                Generated: {new Date(report.generated_at).toLocaleString()}
              </p>
            </div>

            <div className="report-body">
              <ReactMarkdown>{report.report}</ReactMarkdown>
            </div>

            <ExecutionLog
              logs={report.execution_log || []}
              isOpen={logOpen}
              onToggle={() => setLogOpen(!logOpen)}
            />
          </div>
        )}

        {!loading && !report && !error && (
          <div className="empty-state">
            <div className="empty-icon">
              <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
                <rect x="8" y="12" width="48" height="40" rx="4" stroke="#4b5563" strokeWidth="2" />
                <path d="M16 24h32M16 32h24M16 40h28" stroke="#4b5563" strokeWidth="2" strokeLinecap="round" />
                <circle cx="48" cy="16" r="8" fill="#059669" />
                <path d="M45 16h6M48 13v6" stroke="white" strokeWidth="2" strokeLinecap="round" />
              </svg>
            </div>
            <h3>Enter a company name to generate a research report</h3>
            <p>Our AI agents will collect data, analyze financials, and write a professional equity research report.</p>
          </div>
        )}
      </main>
    </div>
  )
}
