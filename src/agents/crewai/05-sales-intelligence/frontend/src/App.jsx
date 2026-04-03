import { useState, useEffect } from 'react'

function App() {
  const [form, setForm] = useState({ name: '', email: '', company: '', title: '', linkedin_url: '', notes: '' })
  const [leads, setLeads] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [expandedLead, setExpandedLead] = useState(null)

  const fetchLeads = async () => {
    const res = await fetch('/leads')
    const data = await res.json()
    setLeads(data.leads || [])
  }

  useEffect(() => { fetchLeads() }, [])

  const handleChange = (field, value) => setForm((prev) => ({ ...prev, [field]: value }))

  const handleSubmit = async () => {
    if (!form.name.trim() || !form.company.trim()) return
    setLoading(true)
    setError('')
    try {
      const res = await fetch('/process-lead', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      })
      if (!res.ok) throw new Error(`Request failed: ${res.status}`)
      await res.json()
      await fetchLeads()
      setForm({ name: '', email: '', company: '', title: '', linkedin_url: '', notes: '' })
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleAction = async (leadId, action) => {
    await fetch(`/${action}/${leadId}`, { method: 'POST' })
    await fetchLeads()
  }

  const statusColor = {
    pending: '#94a3b8', enriching: '#3b82f6', scoring: '#8b5cf6',
    generating_outreach: '#f59e0b', pending_approval: '#f97316',
    approved: '#22c55e', rejected: '#ef4444', archived: '#6b7280',
  }

  return (
    <div className="app">
      <header className="header">
        <h1>Sales Intelligence System</h1>
        <p>Inspired by Clay — AI-powered lead enrichment & outreach</p>
      </header>
      <div className="layout">
        <aside className="sidebar">
          <h2>New Lead</h2>
          <div className="form-stack">
            {['name', 'email', 'company', 'title'].map((field) => (
              <div key={field} className="form-group">
                <label>{field.charAt(0).toUpperCase() + field.slice(1).replace('_', ' ')}</label>
                <input type="text" value={form[field]} onChange={(e) => handleChange(field, e.target.value)} className="text-input" placeholder={field === 'name' ? 'Jane Smith' : field === 'company' ? 'Acme Corp' : ''} />
              </div>
            ))}
            <div className="form-group">
              <label>LinkedIn URL</label>
              <input type="text" value={form.linkedin_url} onChange={(e) => handleChange('linkedin_url', e.target.value)} className="text-input" placeholder="https://linkedin.com/in/..." />
            </div>
            <div className="form-group">
              <label>Notes</label>
              <textarea value={form.notes} onChange={(e) => handleChange('notes', e.target.value)} className="textarea" rows={3} placeholder="Any additional context..." />
            </div>
            <button onClick={handleSubmit} disabled={loading || !form.name.trim() || !form.company.trim()} className="submit-btn">
              {loading ? 'Processing...' : 'Process Lead'}
            </button>
          </div>
          {error && <div className="error-banner">{error}</div>}
        </aside>
        <main className="dashboard">
          <h2>Leads Dashboard ({leads.length})</h2>
          {loading && <div className="loading"><div className="loading-spinner" /><p>Processing lead through the pipeline...</p></div>}
          {leads.length === 0 && !loading && <div className="empty-state"><p>No leads processed yet. Add a lead to get started.</p></div>}
          {leads.map((lead) => (
            <div key={lead.lead_id} className="lead-card" onClick={() => setExpandedLead(expandedLead === lead.lead_id ? null : lead.lead_id)}>
              <div className="lead-header">
                <div className="lead-info">
                  <h3>{lead.name}</h3>
                  <span className="lead-company">{lead.company}</span>
                </div>
                <div className="lead-meta">
                  <div className="score-bar"><div className="score-fill" style={{ width: `${lead.overall_score}%`, background: lead.overall_score >= 70 ? '#22c55e' : lead.overall_score >= 40 ? '#f59e0b' : '#ef4444' }} /><span>{lead.overall_score}</span></div>
                  <span className="status-badge" style={{ background: statusColor[lead.status] || '#94a3b8' }}>{lead.status.replace('_', ' ')}</span>
                </div>
              </div>
              {expandedLead === lead.lead_id && (
                <div className="lead-details">
                  {lead.enrichment_summary && <div className="detail-section"><h4>Enrichment</h4><p>{lead.enrichment_summary}</p></div>}
                  {lead.scoring_rationale && <div className="detail-section"><h4>Scoring Rationale</h4><p>{lead.scoring_rationale.substring(0, 500)}</p></div>}
                  {lead.email_subject && (
                    <div className="detail-section">
                      <h4>Outreach Email</h4>
                      <div className="email-preview">
                        <strong>Subject: {lead.email_subject}</strong>
                        <p>{lead.email_body}</p>
                      </div>
                    </div>
                  )}
                  {lead.status === 'pending_approval' && (
                    <div className="action-buttons">
                      <button className="approve-btn" onClick={(e) => { e.stopPropagation(); handleAction(lead.lead_id, 'approve') }}>Approve</button>
                      <button className="reject-btn" onClick={(e) => { e.stopPropagation(); handleAction(lead.lead_id, 'reject') }}>Reject</button>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </main>
      </div>
    </div>
  )
}

export default App
