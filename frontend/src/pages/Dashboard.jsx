// v2
import { useNavigate } from 'react-router-dom'
import { Zap, Shield, FileText, MessageSquare, FlaskConical, ArrowRight, TrendingUp, Users, AlertTriangle } from 'lucide-react'

const features = [
  {
    to: '/predict',
    icon: Zap,
    color: 'accent',
    title: 'Predict & Explain',
    description: 'Submit a loan application and get an instant AI decision with full SHAP-powered explanation in plain English.',
    tag: 'Core Feature'
  },
  {
    to: '/whatif',
    icon: FlaskConical,
    color: 'emerald',
    title: 'What-If Simulator',
    description: 'Change individual factors and instantly see how your risk score shifts. Find the minimal changes needed to flip a rejection.',
    tag: 'New'
  },
  {
    to: '/bias',
    icon: Shield,
    color: 'amber',
    title: 'Bias Detection',
    description: 'Analyze the AI model for demographic bias across gender, ethnicity, and geography using disparate impact analysis.',
    tag: 'Fairness'
  },
  {
    to: '/appeal',
    icon: FileText,
    color: 'crimson',
    title: 'Decision Appeal',
    description: 'Rejected? Submit an appeal with your reasoning and get AI-powered counterfactual suggestions to flip the decision.',
    tag: 'Appeal'
  },
  {
    to: '/copilot',
    icon: MessageSquare,
    color: 'accent-soft',
    title: 'AI Copilot Chat',
    description: 'Ask the AI anything about your loan decision in plain English. No jargon, no confusion.',
    tag: 'Conversational'
  }
]

const stats = [
  { label: 'Model Accuracy',   value: '94%',     icon: TrendingUp,    color: 'emerald' },
  { label: 'Training Dataset', value: '150,000', icon: Users,         color: 'accent'  },
  { label: 'AUC-ROC Score',    value: '0.87',    icon: AlertTriangle, color: 'amber'   },
]

const colorMap = {
  accent:       'text-accent bg-accent/10 border-accent/20',
  emerald:      'text-emerald bg-emerald/10 border-emerald/20',
  amber:        'text-amber bg-amber/10 border-amber/20',
  'accent-soft':'text-accent-soft bg-accent/10 border-accent/20',
  crimson:      'text-crimson bg-crimson/10 border-crimson/20',
}

export default function Dashboard() {
  const navigate = useNavigate()

  return (
    // ✅ Changed: p-8 → p-4 sm:p-6 md:p-8, added overflow-x-hidden
    <div className="p-4 sm:p-6 md:p-8 max-w-6xl mx-auto animate-slide-up overflow-x-hidden">

      {/* Hero */}
      <div className="mb-8 md:mb-12">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-accent/10 border border-accent/20 text-accent text-xs font-mono mb-4">
          <span className="w-1.5 h-1.5 rounded-full bg-accent animate-pulse-slow" />
          Enterprise AI · Finance · Explainability
        </div>
        {/* ✅ Changed: text-5xl → text-3xl sm:text-4xl md:text-5xl */}
        <h1 className="font-display text-3xl sm:text-4xl md:text-5xl font-800 text-white leading-tight mb-4">
          Explainable AI Copilot
          <br />
          <span className="gradient-text">for Credit Risk</span>
        </h1>
        {/* ✅ Changed: text-lg → text-base sm:text-lg */}
        <p className="text-muted text-base sm:text-lg max-w-2xl leading-relaxed">
          The first loan decision system that explains itself — in plain English.
          Built with SHAP explainability, bias detection, and a natural language appeal system.
        </p>
      </div>

      {/* Stats */}
      {/* ✅ Changed: grid-cols-3 → grid-cols-1 sm:grid-cols-3 */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8 md:mb-10">
        {stats.map(({ label, value, icon: Icon, color }) => (
          // ✅ Changed: p-5 → p-4 sm:p-5, added flex sm:block for horizontal layout on mobile
          <div key={label} className="bg-panel border border-border rounded-2xl p-4 sm:p-5 flex items-center gap-4 sm:block">
            <div className={`w-8 h-8 rounded-lg ${colorMap[color]} flex items-center justify-center border sm:mb-3 shrink-0`}>
              <Icon size={14} />
            </div>
            <div>
              <div className="text-2xl font-display font-700 text-white">{value}</div>
              <div className="text-sm text-muted mt-0.5">{label}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Feature Cards */}
      {/* ✅ Changed: grid-cols-2 → grid-cols-1 sm:grid-cols-2 */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {features.map(({ to, icon: Icon, color, title, description, tag }) => (
          <button
            key={to}
            onClick={() => navigate(to)}
            // ✅ Changed: p-6 → p-4 sm:p-6
            className="bg-panel border border-border rounded-2xl p-4 sm:p-6 text-left hover:border-accent/40 hover:bg-panel/80 transition-all duration-200 group"
          >
            <div className="flex items-start justify-between mb-4">
              <div className={`w-10 h-10 rounded-xl flex items-center justify-center border ${colorMap[color]}`}>
                <Icon size={18} />
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-mono text-muted px-2 py-0.5 bg-border/50 rounded-full">{tag}</span>
                <ArrowRight size={16} className="text-muted group-hover:text-white group-hover:translate-x-0.5 transition-all" />
              </div>
            </div>
            <h3 className="font-display font-600 text-white text-lg mb-2">{title}</h3>
            <p className="text-sm text-muted leading-relaxed">{description}</p>
          </button>
        ))}
      </div>

      {/* Tech stack */}
      {/* ✅ Changed: gap-6 → gap-3 sm:gap-6, added flex-wrap already present ✓ */}
      <div className="mt-6 md:mt-8 p-4 bg-panel border border-border rounded-2xl flex items-center gap-3 sm:gap-6 flex-wrap">
        <span className="text-xs text-muted font-mono">TECH STACK</span>
        {['FastAPI', 'Scikit-learn', 'SHAP', 'Groq · LLaMA 3.3', 'React', 'Recharts'].map(t => (
          <span key={t} className="text-xs font-mono text-accent-soft bg-accent/5 px-2 py-1 rounded-md border border-accent/10">{t}</span>
        ))}
      </div>
    </div>
  )
}
