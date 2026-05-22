import { useState } from 'react'
import { predictLoan, explainDecision } from '../services/api'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { CheckCircle, XCircle, Loader, Zap, ChevronRight } from 'lucide-react'
import toast from 'react-hot-toast'

const defaultForm = {
  revolving_utilization: 0.35,
  age: 45,
  late_30_59_days: 0,
  debt_ratio: 0.28,
  monthly_income: 5400,
  open_credit_lines: 8,
  late_90_days: 0,
  real_estate_loans: 1,
  late_60_89_days: 0,
  num_dependents: 2,
  gender: 'Male', ethnicity: 'White', zip_region: 'Urban'
}

const fields = [
  { key: 'revolving_utilization', label: 'Revolving Utilization (0–1)', type: 'number', min: 0, max: 1, step: 0.01 },
  { key: 'age',                   label: 'Age',                          type: 'number', min: 18, max: 100 },
  { key: 'late_30_59_days',       label: 'Times 30–59 Days Late',        type: 'number', min: 0, max: 20 },
  { key: 'debt_ratio',            label: 'Debt Ratio',                   type: 'number', min: 0, step: 0.01 },
  { key: 'monthly_income',        label: 'Monthly Income ($)',           type: 'number', min: 0, step: 100 },
  { key: 'open_credit_lines',     label: 'Open Credit Lines',            type: 'number', min: 0 },
  { key: 'late_90_days',          label: 'Times 90+ Days Late',          type: 'number', min: 0, max: 20 },
  { key: 'real_estate_loans',     label: 'Real Estate Loans',            type: 'number', min: 0 },
  { key: 'late_60_89_days',       label: 'Times 60–89 Days Late',        type: 'number', min: 0, max: 20 },
  { key: 'num_dependents',        label: 'Number of Dependents',         type: 'number', min: 0 },
]

export default function Predict() {
  const [form, setForm]           = useState(defaultForm)
  const [result, setResult]       = useState(null)
  const [explanation, setExpl]    = useState(null)
  const [loading, setLoading]     = useState(false)
  const [explaining, setExplaining] = useState(false)

  const handleChange = (key, val) =>
    setForm(f => ({ ...f, [key]: parseFloat(val) ?? val }))

  const handlePredict = async () => {
    setLoading(true); setResult(null); setExpl(null)
    try {
      const res = await predictLoan(form)
      setResult(res)
      toast.success('Prediction complete!')
      setExplaining(true)
      const exp = await explainDecision(form)
      setExpl(exp)
    } catch (e) {
      toast.error('API Error: ' + (e.response?.data?.detail || e.message))
    } finally {
      setLoading(false); setExplaining(false)
    }
  }

  const isRejected = result?.decision === 'Rejected'

  return (
    <div className="p-8 max-w-6xl mx-auto animate-slide-up">
      <div className="mb-8">
        <h1 className="font-display text-3xl font-700 text-white mb-2">Predict & Explain</h1>
        <p className="text-muted">Submit an application. Get a decision + SHAP-powered explanation.</p>
      </div>

      <div className="grid grid-cols-2 gap-6">
        {/* Form */}
        <div className="bg-panel border border-border rounded-2xl p-6">
          <h2 className="font-display font-600 text-white mb-5">Loan Application</h2>
          <div className="space-y-4">
            {fields.map(({ key, label, type, min, max, step }) => (
              <div key={key}>
                <label className="text-xs font-mono text-muted block mb-1.5">{label}</label>
                <input
                  type={type} min={min} max={max} step={step || 1}
                  value={form[key]}
                  onChange={e => handleChange(key, e.target.value)}
                  className="w-full bg-ink border border-border rounded-xl px-3 py-2.5 text-sm text-white focus:outline-none focus:border-accent transition-colors"
                />
              </div>
            ))}

            <div className="pt-2 border-t border-border">
              <p className="text-xs text-muted font-mono mb-3">DEMOGRAPHIC (bias analysis only)</p>
              <div className="grid grid-cols-3 gap-2">
                {[
                  { key: 'gender',     opts: ['Male', 'Female'] },
                  { key: 'ethnicity',  opts: ['White', 'Black', 'Hispanic', 'Asian', 'Other'] },
                  { key: 'zip_region', opts: ['Urban', 'Suburban', 'Rural'] }
                ].map(({ key, opts }) => (
                  <select key={key} value={form[key]}
                    onChange={e => handleChange(key, e.target.value)}
                    className="bg-ink border border-border rounded-xl px-2 py-2 text-xs text-white focus:outline-none focus:border-accent"
                  >
                    {opts.map(o => <option key={o}>{o}</option>)}
                  </select>
                ))}
              </div>
            </div>
          </div>

          <button onClick={handlePredict} disabled={loading}
            className="w-full mt-6 bg-accent hover:bg-accent/80 disabled:opacity-50 text-white font-display font-600 py-3 rounded-xl flex items-center justify-center gap-2 transition-all"
          >
            {loading ? <Loader size={16} className="animate-spin" /> : <Zap size={16} />}
            {loading ? 'Analyzing...' : 'Analyze Application'}
          </button>
        </div>

        {/* Results */}
        <div className="space-y-4">
          {result && (
            <div className={`rounded-2xl p-6 border animate-slide-up ${
              isRejected ? 'bg-crimson/5 border-crimson/30' : 'bg-emerald/5 border-emerald/30'
            }`}>
              <div className="flex items-center gap-3 mb-4">
                {isRejected ? <XCircle size={28} className="text-crimson" /> : <CheckCircle size={28} className="text-emerald" />}
                <div>
                  <div className="font-display font-700 text-xl text-white">{result.decision}</div>
                  <div className="text-xs text-muted font-mono">Confidence: {result.confidence}</div>
                </div>
                <div className="ml-auto text-right">
                  <div className={`text-3xl font-display font-700 ${isRejected ? 'text-crimson' : 'text-emerald'}`}>
                    {result.risk_score}
                  </div>
                  <div className="text-xs text-muted">Risk Score /100</div>
                </div>
              </div>
              <div className="bg-black/20 rounded-xl p-3">
                <div className="text-xs text-muted font-mono mb-1">DEFAULT PROBABILITY</div>
                <div className="h-2 bg-border rounded-full overflow-hidden">
                  <div className={`h-full rounded-full transition-all ${isRejected ? 'bg-crimson' : 'bg-emerald'}`}
                    style={{ width: `${result.probability_default * 100}%` }} />
                </div>
                <div className="text-xs text-muted font-mono mt-1">{(result.probability_default * 100).toFixed(1)}%</div>
              </div>
            </div>
          )}

          {explanation && (
            <div className="bg-panel border border-border rounded-2xl p-6 animate-slide-up">
              <h3 className="font-display font-600 text-white mb-4">SHAP Feature Impact</h3>
              <ResponsiveContainer width="100%" height={240}>
                <BarChart
                  data={explanation.feature_contributions.slice(0, 6).map(c => ({
                    name: c.feature.replace(/_/g, ' '),
                    value: parseFloat(c.shap_value.toFixed(4)),
                  }))}
                  layout="vertical" margin={{ left: 20 }}
                >
                  <XAxis type="number" tick={{ fontSize: 10, fill: '#6B7080' }} />
                  <YAxis dataKey="name" type="category" tick={{ fontSize: 10, fill: '#6B7080' }} width={140} />
                  <Tooltip formatter={(v) => [v.toFixed(4), 'SHAP Value']}
                    contentStyle={{ background: '#1A1A25', border: '1px solid #2A2A3A', borderRadius: 8, fontSize: 12 }} />
                  <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                    {explanation.feature_contributions.slice(0, 6).map((c, i) => (
                      <Cell key={i} fill={c.shap_value > 0 ? '#FF4D6A' : '#00D48A'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
              <div className="flex gap-4 mt-2">
                <span className="text-xs text-muted flex items-center gap-1"><span className="w-3 h-2 bg-crimson rounded inline-block" /> Increases Risk</span>
                <span className="text-xs text-muted flex items-center gap-1"><span className="w-3 h-2 bg-emerald rounded inline-block" /> Decreases Risk</span>
              </div>
            </div>
          )}

          {(explaining || explanation) && (
            <div className="bg-panel border border-border rounded-2xl p-6 animate-slide-up">
              <div className="flex items-center gap-2 mb-3">
                <div className="w-6 h-6 rounded-lg bg-accent/20 flex items-center justify-center">
                  <ChevronRight size={12} className="text-accent" />
                </div>
                <span className="text-xs font-mono text-muted">AI EXPLANATION · LLaMA 3 70B</span>
              </div>
              {explaining && !explanation
                ? <div className="text-muted text-sm animate-pulse-slow">Generating explanation...</div>
                : <p className="text-sm text-white/80 leading-relaxed">{explanation?.plain_english}</p>
              }
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
