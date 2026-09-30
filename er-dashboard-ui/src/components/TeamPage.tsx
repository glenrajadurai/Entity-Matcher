import React from 'react';
import { User, Code, Database, Cpu } from 'lucide-react';

export const TeamPage: React.FC = () => {
  const members = [
    { name: 'Member 1', role: 'Data Analysis & Preprocessing', icon: Database, desc: 'Responsible for raw dataset cleaning, noise analysis, and open-set attribute normalization across S1/S2/S3.', color: 'text-indigo-400' },
    { name: 'Member 2', role: 'Candidate Generation & Feature Engineering', icon: Code, desc: 'Responsible for multi-pass candidate blocking rules and extracting pairwise string/address similarity feature tables.', color: 'text-purple-400' },
    { name: 'Member 3', role: 'Machine Learning, Model Comparison & Evaluation', icon: Cpu, desc: 'Responsible for leakage-safe GroupShuffleSplit, model comparison (LightGBM/XGBoost/CatBoost), precision threshold tuning, and error taxonomy.', color: 'text-emerald-400' },
  ];

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold text-white">Team Member Contributions</h2>
        <p className="text-slate-400 mt-1">
          Responsibilities and ownership breakdown across the Business Entity Resolution challenge.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {members.map((m, idx) => {
          const Icon = m.icon;
          return (
            <div key={idx} className="bg-[#172036] border border-slate-800 p-6 rounded-2xl space-y-4">
              <div className="flex items-center gap-3">
                <div className={`w-10 h-10 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-center font-bold ${m.color}`}>
                  <Icon className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-white">{m.name}</h3>
                  <p className="text-xs text-slate-400 font-medium">{m.role}</p>
                </div>
              </div>
              <p className="text-sm text-slate-300 leading-relaxed">{m.desc}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
};
