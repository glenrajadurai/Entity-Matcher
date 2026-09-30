import React from 'react';
import { 
  LayoutDashboard, 
  Database, 
  BarChart3, 
  AlertTriangle, 
  Sparkles, 
  Search, 
  ShieldCheck, 
  CheckCircle2, 
  GitFork, 
  Users 
} from 'lucide-react';

export type NavTab = 
  | 'dashboard' 
  | 'data-overview' 
  | 'model-performance' 
  | 'error-analysis' 
  | 'research-improvement' 
  | 'entity-matching' 
  | 'robustness' 
  | 'final-results' 
  | 'architecture' 
  | 'team';

interface SidebarProps {
  activeTab: NavTab;
  setActiveTab: (tab: NavTab) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab }) => {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'data-overview', label: 'Data Overview', icon: Database },
    { id: 'model-performance', label: 'Model Performance', icon: BarChart3 },
    { id: 'error-analysis', label: 'Error Analysis', icon: AlertTriangle },
    { id: 'research-improvement', label: 'Research Improvement', icon: Sparkles },
    { id: 'entity-matching', label: 'Entity Matching Demo', icon: Search },
    { id: 'robustness', label: 'Robustness Stress Test', icon: ShieldCheck },
    { id: 'final-results', label: 'Final Linkage Results', icon: CheckCircle2 },
    { id: 'architecture', label: 'System Architecture', icon: GitFork },
    { id: 'team', label: 'Team Contributions', icon: Users },
  ];

  return (
    <aside className="w-64 bg-[#0f172a] border-r border-slate-800 flex flex-col h-screen sticky top-0 shrink-0">
      <div className="p-6 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-500 to-emerald-400 flex items-center justify-center font-bold text-white shadow-lg shadow-indigo-500/20">
            ER
          </div>
          <div>
            <h1 className="font-bold text-white text-base leading-tight">Entity Resolution</h1>
            <p className="text-xs text-indigo-400 font-medium">ML Analytics Platform</p>
          </div>
        </div>
      </div>

      <nav className="flex-1 overflow-y-auto p-4 space-y-1">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id as NavTab)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm transition-all duration-200 ${
                isActive
                  ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`}
            >
              <Icon className={`w-5 h-5 ${isActive ? 'text-white' : 'text-slate-400'}`} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      <div className="p-4 border-t border-slate-800 text-xs text-slate-500 text-center">
        Empirical Evaluation Engine v1.0
      </div>
    </aside>
  );
};
