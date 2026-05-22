import { useState } from 'react'
import { submitAppeal } from '../services/api'
import { FileText, Loader, ArrowRight, ChevronRight } from 'lucide-react'
import toast from 'react-hot-toast'

const defaultApp = {
  age: 35, annual_income: 45000, loan_amount: 25000,
  credit_score: 610, employment_years: 2, debt_to_income_ratio: 0.48,
  num_credit_lines: 3, num_delinquencies: 1,
  gender: 'Female', ethnicity: 'Black', zip_region: 'Rural'
}

export default function Appeal() {
  const [application, setApplication] = useState(defaultApp)
  const [appealReason, setAppealReason] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleChange = (key, val) =>
    setApplication(a => ({ ...a, [key]: parseFloat(val) || val }))

  const handleSubmit = async () => {
    if (!appealReason.trim()) {
      toast.error('Please provide an appeal reason.')
      return
    }
    setLoading(true)
    setResult(null)
    try {
      const res = await submitAppeal({
        original_application: application,
        appeal_reason: appealReason
      })
      setResult(res)
      toast.success('Appeal processed!')
    } catch (e) {
      toast.error('Error: ' + (e.response?.data?.detail || e.message))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-8 max-w-6xl mx-auto animate-slide-up">
      <div className="mb-8">
        <h1 className="font-display text-3xl font-700 text-white mb-2">Decision Appeal</h1>
        <p className="text-muted">Rejected? Submit your appeal and get AI-powered counterfactual analysis.</p>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="space-y-4">
          <div className="bg-panel border border-border rounded-2xl p-6">
            <h2 className="font-display font-600 text-white mb-4">Original Application</h2>
            <div className="grid grid-cols-2 gap-3">
              {[
                { key: 'credit_score', label: 'Credit Score' },
                { key: 'annual_income', label: 'Annual Income ($)' },
                { key: 'loan_amount', label: 'Loan Amount ($)' },
                { key: 'debt_to_income_ratio', label: 'DTI Ratio' },
                { key: 'employment_years', label: 'Employment Yrs' },
                { key: 'num_delinquencies', label: 'Delinquencies' },
              ].map(({ key, label }) => (
                <div key={key}>
                  <label className="text-xs font-mono text-muted block mb-1">{label}</label>
                  <input
                    type="number"
                    value={application[key]}
                    step={key === 'debt_to_income_ratio' ? 0.01 : 1}
                    onChange={e => handleChange(key, e.target.value)}
                    className="w-full bg-ink border border-border rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-accent transition-colors"
                  />
                </div>
              ))}
            </div>
          </div>

          <div className="bg-panel border border-border rounded-2xl p-6">
            <h2 className="font-display font-600 text-white mb-3">Your Appeal Reason</h2>
            <textarea
              value={appealReason}
              onChange={e => setAppealReason(e.target.value)}
              rows={4}
              placeholder="Explain why you believe this decision should be reconsidered..."
              className="w-full bg-ink border border-border rounded-xl px-3 py-2.5 text-sm text-white focus:outline-none focus:border-accent transition-colors resize-none placeholder:text-muted"
            />
            <button
              onClick={handleSubmit}
              disabled={loading}
              className="w-full mt-4 bg-amber/90 hover:bg-amber disabled:opacity-50 text-ink font-display font-600 py-3 rounded-xl flex items-center justify-center gap-2 transition-all"
            >
              {loading ? <Loader size={16} className="animate-spin" /> : <FileText size={16} />}
              {loading ? 'Processing Appeal...' : 'Submit Appeal'}
            </button>
          </div>
        </div>

        <div className="space-y-4">
          {!result && !loading && (
            <div className="bg-panel border border-border border-dashed rounded-2xl p-12 flex flex-col items-center justify-center text-center">
              <FileText size={32} className="text-muted mb-3" />
              <p className="text-muted text-sm">Submit your appeal to see<br />AI-powered counterfactual analysis</p>
            </div>
          )}

          {loading && (
            <div className="bg-panel border border-border rounded-2xl p-12 flex flex-col items-center justify-center text-center">
              <Loader size={28} className="text-accent animate-spin mb-3" />
              <p className="text-muted text-sm">Analyzing your appeal...</p>
            </div>
          )}

          {result && (
            <>
              <div className="bg-panel border border-border rounded-2xl p-6 animate-slide-up">
                <h3 className="font-display font-600 text-white mb-4">Appeal Outcome</h3>
                <div className="flex items-center gap-4">
                  <div className="flex-1 bg-ink rounded-xl p-4 text-center">
                    <div className="text-xs font-mono text-muted mb-1">ORIGINAL</div>
                    <div className={`font-display font-700 text-lg ${result.original_decision === 'Rejected' ? 'text-crimson' : 'text-emerald'}`}>
                      {result.original_decision}
                    </div>
                  </div>
                  <ArrowRight size={20} className="text-muted flex-shrink-0" />
                  <div className="flex-1 bg-ink rounded-xl p-4 text-center">
                    <div className="text-xs font-mono text-muted mb-1">APPEAL</div>
                    <div className={`font-display font-700 text-lg ${result.appeal_decision === 'Rejected' ? 'text-crimson' : 'text-emerald'}`}>
                      {result.appeal_decision}
                    </div>
                  </div>
                </div>
                {result.changed && (
                  <div className="mt-3 text-center text-xs text-emerald font-mono">✓ Decision reversed on appeal</div>
                )}
              </div>

              {result.what_would_flip_decision.length > 0 && (
                <div className="bg-panel border border-border rounded-2xl p-6 animate-slide-up">
                  <h3 className="font-display font-600 text-white mb-3">What Would Flip the Decision</h3>
                  <p className="text-xs text-muted mb-3">Counterfactual analysis — minimal changes needed for approval:</p>
                  <div className="space-y-2">
                    {result.what_would_flip_decision.map((item, i) => (
                      <div key={i} className="flex items-start gap-2 text-sm text-white/80 bg-accent/5 border border-accent/15 rounded-xl p-3">
                        <ChevronRight size={14} className="text-accent mt-0.5 flex-shrink-0" />
                        {item}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="bg-panel border border-border rounded-2xl p-6 animate-slide-up">
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-6 h-6 rounded-lg bg-accent/20 flex items-center justify-center">
                    <ChevronRight size={12} className="text-accent" />
                  </div>
                  <span className="text-xs font-mono text-muted">AI APPEAL RESPONSE</span>
                </div>
                <p className="text-sm text-white/80 leading-relaxed">{result.ai_response}</p>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
