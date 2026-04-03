import { useState } from 'react'

function App() {
  const [resumeText, setResumeText] = useState('')
  const [jobUrl, setJobUrl] = useState('')
  const [jobDescription, setJobDescription] = useState('')
  const [companyName, setCompanyName] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [activeTab, setActiveTab] = useState('company')

  const handleSubmit = async () => {
    if (!resumeText.trim()) return
    setLoading(true)
    setError('')
    setResult(null)
    try {
      const res = await fetch('/apply', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          resume_text: resumeText,
          job_url: jobUrl,
          job_description: jobDescription,
          company_name: companyName,
        }),
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

  const scoreColor = (score) => {
    if (score >= 75) return '#059669'
    if (score >= 50) return '#d97706'
    return '#dc2626'
  }

  return (
    <div className="app">
      <header className="header">
        <h1>Job Application Toolkit</h1>
        <p>Inspired by Teal — AI-powered resume tailoring & cover letters</p>
      </header>
      <div className="layout">
        <div className="input-panel">
          <h2>Your Application</h2>
          <label>Company Name</label>
          <input
            type="text"
            value={companyName}
            onChange={(e) => setCompanyName(e.target.value)}
            placeholder="e.g., Stripe"
            className="text-input"
          />
          <label>Job Posting URL</label>
          <input
            type="text"
            value={jobUrl}
            onChange={(e) => setJobUrl(e.target.value)}
            placeholder="https://..."
            className="text-input"
          />
          <label>Job Description (optional if URL provided)</label>
          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste the job description here..."
            className="textarea"
            rows={6}
          />
          <label>Your Resume</label>
          <textarea
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
            placeholder="Paste your resume text here..."
            className="textarea"
            rows={10}
          />
          <button
            onClick={handleSubmit}
            disabled={loading || !resumeText.trim()}
            className="submit-btn"
          >
            {loading ? 'Generating...' : 'Generate Application Package'}
          </button>
        </div>
        <div className="output-panel">
          {error && <div className="error-banner">{error}</div>}
          {loading && (
            <div className="loading">
              <div className="loading-spinner" />
              <p>Building your application package...</p>
            </div>
          )}
          {result && (
            <>
              <div className="score-badge" style={{ background: scoreColor(result.overall_match_score) }}>
                {result.overall_match_score}% Match
              </div>
              <div className="tabs">
                {['company', 'resume', 'cover'].map((tab) => (
                  <button
                    key={tab}
                    className={`tab ${activeTab === tab ? 'active' : ''}`}
                    onClick={() => setActiveTab(tab)}
                  >
                    {tab === 'company' ? 'Company Profile' : tab === 'resume' ? 'Tailored Resume' : 'Cover Letter'}
                  </button>
                ))}
              </div>
              <div className="tab-content">
                {activeTab === 'company' && (
                  <div>
                    <h3>{result.company_profile.company_name || 'Company'}</h3>
                    <p><strong>Industry:</strong> {result.company_profile.industry}</p>
                    <p><strong>Size:</strong> {result.company_profile.company_size}</p>
                    {result.company_profile.culture_values.length > 0 && (
                      <div className="tags-section">
                        <strong>Culture & Values</strong>
                        <div className="tags">{result.company_profile.culture_values.map((v, i) => <span key={i} className="tag">{v}</span>)}</div>
                      </div>
                    )}
                    {result.company_profile.tech_stack.length > 0 && (
                      <div className="tags-section">
                        <strong>Tech Stack</strong>
                        <div className="tags">{result.company_profile.tech_stack.map((t, i) => <span key={i} className="tag tech">{t}</span>)}</div>
                      </div>
                    )}
                    {result.company_profile.key_requirements.length > 0 && (
                      <div><strong>Key Requirements</strong><ul>{result.company_profile.key_requirements.map((r, i) => <li key={i}>{r}</li>)}</ul></div>
                    )}
                  </div>
                )}
                {activeTab === 'resume' && (
                  <div>
                    <h3>Optimized Summary</h3>
                    <p>{result.tailored_resume.optimized_summary}</p>
                    {result.tailored_resume.highlighted_skills.length > 0 && (
                      <div className="tags-section">
                        <strong>Highlighted Skills</strong>
                        <div className="tags">{result.tailored_resume.highlighted_skills.map((s, i) => <span key={i} className="tag">{s}</span>)}</div>
                      </div>
                    )}
                    {result.tailored_resume.keyword_matches.length > 0 && (
                      <div className="tags-section">
                        <strong>Keyword Matches</strong>
                        <div className="tags">{result.tailored_resume.keyword_matches.map((k, i) => <span key={i} className="tag tech">{k}</span>)}</div>
                      </div>
                    )}
                    {result.tailored_resume.suggestions.length > 0 && (
                      <div><strong>Suggestions</strong><ul>{result.tailored_resume.suggestions.map((s, i) => <li key={i}>{s}</li>)}</ul></div>
                    )}
                  </div>
                )}
                {activeTab === 'cover' && (
                  <div className="cover-letter">
                    <h3>{result.cover_letter.subject_line}</h3>
                    <div className="letter-body">{result.cover_letter.body}</div>
                    {result.cover_letter.key_talking_points.length > 0 && (
                      <div><strong>Key Talking Points</strong><ul>{result.cover_letter.key_talking_points.map((p, i) => <li key={i}>{p}</li>)}</ul></div>
                    )}
                  </div>
                )}
              </div>
            </>
          )}
          {!result && !loading && !error && (
            <div className="empty-state">
              <p>Fill in your resume and job details, then click Generate to get your tailored application package.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
