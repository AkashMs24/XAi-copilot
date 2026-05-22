import { useState } from 'react'
import { runWhatIf } from '../services/api'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine, Cell } from 'recharts'
import { Plus, Trash2, Loader, FlaskConical, TrendingDown, TrendingUp } from 'lucide-react'
import toast from 'react-hot-toast'

const FIELDS = [
  { key: 'revolving_utilization', label: 'Revolving Utilization', type: 'float', min: 0,  max: 1,     step: 0.01 },
  { key: 'age',                   label: 'Age',                   type: 'int',   min: 18, max: 100,   step: 1    },
  { key: 'late_30_59_days',       label: '30–59 Days Late',       type: 'int',   min: 0,  max: 20,    step: 1    },
  { key: 'debt_ratio',            label: 'Debt Ratio',            type: 'float', min: 0,  max: 5,     step: 0.01 },
  { key: 'monthly_income',        label: 'Monthly Income ($)',    type: 'float', min: 0,  max: 50000, step: 100  },
  { key: 'open_credit_lines',     label: 'Open Credit Lines',     type: 'int',   min: 0,  max: 60,    step: 1    },
  { key: 'late_90_days',          label: '90+ Days Late',         type: 'int',   min: 0,  max: 20,    step: 1    },
  { key: 'real_estate_loans',     label: 'Real Estate Loans',     type: 'int',   min: 0,  max: 20,    step: 1    },
  { key: 'late_60_89_days',       label: '60–89 Days Late',       type: 'int',   min: 0,  max: 20,    step: 1    },
  { key: 'num_dependents',        label: 'Dependents',            type: 'int',   min: 0,  max: 20,    step: 1    },
]

const BASE_DEFAULT = {
  revolving_utilization: 0.65,
  age: 45,
  late_30_59_days: 2,
  debt_ratio: 0.5,
  monthly_income: 4000,
  open_credit_lines: 6,
  late_90_days: 1,
  real_estate_loans: 1,
  late_60_89_days: 0,
  num_dependents: 2,
  gender: 'Male', ethnicity: 'White', zip_region: 'Urban'
}

const emptyScenario = () => ({ field: 'revolving_utilization', value: '' })

export default function WhatIf() {
  const [base, setBase]             = useState(BASE_DEFAULT)
  const [scenarios, setScenarios]   = useState([emptyScenario()])
  const [result, setResult]         = useState(null)
  const [loading, setLoading]       = useState(false)

  // ── base form ──────────────────────────────────────────────────────────────
  const handleBase = (key, raw) => {
    const f = FIELDS.find(f => f.key === key)
    const v = f?.type === 'int' ? parseInt(raw) : parseFloat(raw)
    setBase(b => ({ ...b, [key]: isNaN(v) ? raw : v }))
  }

  // ── scenarios ──────────────────────────────────────────────────────────────
  const addScenario    = ()  => setScenarios(s => [...s, emptyScenario()])
  const removeScenario = (i) => setScenarios(s => s.filter((_, idx) => idx !== i))
  const updateScenario = (i, key, val) =>
    setScenarios(s => s.map((sc, idx) => idx === i ? { ...sc, [key]: val } : sc))

  // ── run ────────────────────────────────────────────────────────────────────
  const handleRun = async () => {
    const built = scenarios.map(sc => {
      const f = FIELDS.find(f => f.key === sc.field)
      const v = f?.type === 'int' ? parseInt(sc.value) : parseFloat(sc.value)
      return { [sc.field]: isNaN(v) ? sc.value : v }
    }).filter(s => {
      const v = Object.values(s)[0]
      return v !== '' && !isNaN(v)
    })

    if (!built.length) { toast.error('Add at least one valid scenario.'); return }

    setLoading(true); setResult(null)
    try {
      const res = await runWhatIf({ base_application: base, scenarios: built })
      setResult(res)
      toast.success('Scenarios simulated!')
    } catch (e) {
      toast.error(e.response?.data?.detail || e.message)
    } finally {
      setLoading(false)
    }
  }

  // ── chart data ─────────────────────────────────────────────────────────────
  const chartData = result
    ? [
        { name: 'Baseline', risk: result.base_risk_score, delta: 0, decision: result.base_decision },
        ...result.scenarios.map((s, i) => ({
          name: `S${i + 1}: ${Object.keys(s.changes)[0]?.replace(/_/g, ' ')}`,
          risk: s.risk_score,
          delta: s.delta_risk,
          decision: s.decision,
          flipped: s.flipped,
        }))
      ]
    : []

  return (
    <div className="p-8 max-w-6xl mx-auto animate-slide-up">
      <div className="mb-8">
        <h1 className="font-display text-3xl font-700 text-white mb-2 flex items-center gap-3">
          <FlaskConical size={28} className="text-accent" /> What-If Simulator
        </h1>
        <p className="text-muted">Change one or more fields and instantly see how risk score shifts. Find what it takes to flip a rejection.</p>
      </div>

      <div className="grid grid-cols-2 gap-6">
        {/* Left: Base + Scenarios */}
        <div className="space-y-5">
          {/* Base Application */}
          <div className="bg-panel border border-border rounded-2xl p-6">
            <h2 className="font-display font-600 text-white mb-4">Base Application</h2>
            <div className="grid grid-cols-2 gap-3">
              {FIELDS.map(({ key, label, min, max, step }) => (
                <div key={key}>
                  <label className="text-xs font-mono text-muted block mb-1">{label}</label>
                  <input
                    type="number" min={min} max={max} step={step}
                    value={base[key]}
                    onChange={e => handleBase(key, e.target.value)}
                    className="w-full bg-ink border border-border rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-accent transition-colors"
                  />
                </div>
              ))}
            </div>
          </div>

          {/* Scenarios */}
          <div className="bg-panel border border-border rounded-2xl p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-display font-600 text-white">Scenarios to Test</h2>
              <button onClick={addScenario}
                className="flex items-center gap-1 text-xs text-accent hover:text-white border border-accent/30 hover:border-accent rounded-lg px-2.5 py-1.5 transition-all">
                <Plus size={13} /> Add Scenario
              </button>
            </div>

            <div className="space-y-3">
              {scenarios.map((sc, i) => (
                <div key={i} className="flex gap-2 items-center">
                  <div className="w-6 h-6 rounded-lg bg-accent/10 flex items-center justify-center flex-shrink-0">
                    <span className="text-xs font-mono text-accent">S{i + 1}</span>
                  </div>
                  <select
                    value={sc.field}
                    onChange={e => updateScenario(i, 'field', e.target.value)}
                    className="flex-1 bg-ink border border-border rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-accent"
                  >
                    {FIELDS.map(f => <option key={f.key} value={f.key}>{f.label}</option>)}
                  </select>
                  <input
                    type="number"
                    placeholder={`New value`}
                    value={sc.value}
                    onChange={e => updateScenario(i, 'value', e.target.value)}
                    className="w-28 bg-ink border border-border rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-accent"
                  />
                  <button onClick={() => removeScenario(i)} disabled={scenarios.length === 1}
                    className="text-muted hover:text-crimson disabled:opacity-30 transition-colors">
                    <Trash2 size={14} />
                  </button>
                </div>
              ))}
            </div>

            <button onClick={handleRun} disabled={loading}
              className="w-full mt-5 bg-accent hover:bg-accent/80 disabled:opacity-50 text-white font-display font-600 py-3 rounded-xl flex items-center justify-center gap-2 transition-all"
            >
              {loading ? <Loader size={16} className="animate-spin" /> : <FlaskConical size={16} />}
              {loading ? 'Simulating...' : 'Run Scenarios'}
            </button>
          </div>
        </div>

        {/* Right: Results */}
        <div className="space-y-4">
          {result && (
            <>
              {/* Summary */}
              <div className="bg-panel border border-border rounded-2xl p-5">
                <div className="flex items-center gap-3 mb-3">
                  <div className={`px-3 py-1 rounded-full text-xs font-mono font-600 ${
                    result.base_decision === 'Rejected' ? 'bg-crimson/10 text-crimson' : 'bg-emerald/10 text-emerald'
                  }`}>
                    BASE: {result.base_decision}
                  </div>
                  <span className="text-sm text-muted">Risk: <span className="text-white font-600">{result.base_risk_score}</span>/100</span>
                  <span className="text-sm text-muted ml-auto">P(default): <span className="text-white">{(result.base_probability * 100).toFixed(1)}%</span></span>
                </div>
                <p className="text-sm text-white/80">{result.summary}</p>
              </div>

              {/* Risk Score Chart */}
              <div className="bg-panel border border-border rounded-2xl p-5">
                <h3 className="font-display font-600 text-white mb-4">Risk Score by Scenario</h3>
                <ResponsiveContainer width="100%" height={200}>
                  <BarChart data={chartData} margin={{ left: 0 }}>
                    <XAxis dataKey="name" tick={{ fontSize: 9, fill: '#6B7080' }} />
                    <YAxis domain={[0, 100]} tick={{ fontSize: 10, fill: '#6B7080' }} />
                    <Tooltip
                      formatter={(v, n, p) => [v, 'Risk Score']}
                      contentStyle={{ background: '#1A1A25', border: '1px solid #2A2A3A', borderRadius: 8, fontSize: 12 }}
                    />
                    <ReferenceLine y={50} stroke="#6B7080" strokeDasharray="4 4" label={{ value: 'Threshold', fill: '#6B7080', fontSize: 9 }} />
                    <Bar dataKey="risk" radius={[4, 4, 0, 0]}>
                      {chartData.map((d, i) => (
                        <Cell key={i} fill={d.decision === 'Rejected' ? '#FF4D6A' : '#00D48A'} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>

              {/* Scenario Cards */}
              <div className="space-y-2">
                {result.scenarios.map((s, i) => {
                  const improved = s.delta_risk < 0
                  return (
                    <div key={i} className={`rounded-xl p-4 border flex items-center gap-4 ${
                      s.flipped
                        ? 'bg-emerald/5 border-emerald/30'
                        : improved
                        ? 'bg-amber-500/5 border-amber-500/20'
                        : 'bg-panel border-border'
                    }`}>
                      <div className="w-8 h-8 rounded-lg bg-black/20 flex items-center justify-center flex-shrink-0">
                        <span className="text-xs font-mono text-accent">S{i + 1}</span>
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="text-xs font-mono text-muted truncate">
                          {Object.entries(s.changes).map(([k, v]) => `${k.replace(/_/g,' ')} → ${v}`).join(', ')}
                        </div>
                        <div className="flex items-center gap-2 mt-1">
                          <span className={`text-sm font-600 ${s.decision === 'Rejected' ? 'text-crimson' : 'text-emerald'}`}>
                            {s.decision}
                          </span>
                          {s.flipped && <span className="text-xs bg-emerald/20 text-emerald px-2 py-0.5 rounded-full">Decision Flipped ✓</span>}
                        </div>
                      </div>
                      <div className="text-right flex-shrink-0">
                        <div className="text-lg font-display font-700 text-white">{s.risk_score}</div>
                        <div className={`text-xs font-mono flex items-center justify-end gap-1 ${s.delta_risk < 0 ? 'text-emerald' : 'text-crimson'}`}>
                          {s.delta_risk < 0
                            ? <TrendingDown size={10} />
                            : <TrendingUp size={10} />}
                          {s.delta_risk > 0 ? '+' : ''}{s.delta_risk}
                        </div>
                      </div>
                    </div>
                  )
                })}
              </div>
            </>
          )}

          {!result && !loading && (
            <div className="bg-panel border border-border rounded-2xl p-10 flex flex-col items-center text-center gap-3">
              <FlaskConical size={40} className="text-muted/40" />
              <p className="text-muted text-sm">Configure a base application and scenarios,<br />then run the simulator to see risk deltas.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
