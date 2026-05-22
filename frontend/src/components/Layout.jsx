import { Outlet, NavLink } from 'react-router-dom'
import { Brain, BarChart3, Shield, MessageSquare, FileText, Zap, FlaskConical } from 'lucide-react'

const navItems = [
  { to: '/',        label: 'Dashboard',       icon: BarChart3,     exact: true },
  { to: '/predict', label: 'Predict & Explain', icon: Zap },
  { to: '/whatif',  label: 'What-If Simulator', icon: FlaskConical },
  { to: '/bias',    label: 'Bias Detection',   icon: Shield },
  { to: '/appeal',  label: 'Decision Appeal',  icon: FileText },
  { to: '/copilot', label: 'AI Copilot Chat',  icon: MessageSquare },
]

export default function Layout() {
  return (
    <div className="flex min-h-screen bg-ink">
      {/* Sidebar */}
      <aside className="w-64 flex-shrink-0 bg-surface border-r border-border flex flex-col">
        <div className="p-6 border-b border-border">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-accent flex items-center justify-center glow-accent">
              <Brain size={18} className="text-white" />
            </div>
            <div>
              <div className="font-display font-700 text-sm text-white leading-tight">XAI Copilot</div>
              <div className="text-xs text-muted font-mono">Credit Risk Engine</div>
            </div>
          </div>
        </div>

        <nav className="flex-1 p-4 space-y-1">
          {navItems.map(({ to, label, icon: Icon, exact }) => (
            <NavLink key={to} to={to} end={exact}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-body transition-all duration-200 ${
                  isActive
                    ? 'bg-accent/15 text-accent-soft border border-accent/30'
                    : 'text-muted hover:text-white hover:bg-panel'
                }`
              }
            >
              <Icon size={16} />
              {label}
            </NavLink>
          ))}
        </nav>

        <div className="p-4 border-t border-border">
          <div className="text-xs text-muted text-center font-mono">
            Powered by Groq · LLaMA 3 70B
          </div>
        </div>
      </aside>

      <main className="flex-1 overflow-auto">
        <Outlet />
      </main>
    </div>
  )
}
