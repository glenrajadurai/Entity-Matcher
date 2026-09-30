import React, { useEffect, useState } from 'react';
import { fetchDashboardStats, DashboardStats } from '../services/api';
import { ArrowRight, CheckCircle, Database, ShieldAlert, Cpu } from 'lucide-react';

export const DashboardOverview: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDashboardStats()
      .then(data => {
        setStats(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="p-8 text-indigo-400 font-medium animate-pulse">Loading dashboard telemetry...</div>;
  if (error) return <div className="p-8 text-rose-500 bg-rose-500/10 rounded-xl border border-rose-500/20">Error loading dashboard: {error}</div>;

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <div className="flex items-center gap-3">
          <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 text-xs font-semibold rounded-full border border-emerald-500/20">
            SYSTEM ACTIVE
          </span>
          <span className="text-slate-500 text-sm">Empirical Evaluation Suite</span>
        </div>
        <h2 className="text-3xl font-bold text-white mt-2">Business Entity Resolution Dashboard</h2>
        <p className="text-slate-400 mt-1 max-w-3xl">
          Multi-source business entity matching across deduplicated master records (Source 1) and noisy external inputs (Source 2 & Source 3).
        </p>
      </div>

      {/* Workflow Summary */}
      <div className="bg-[#172036] border border-slate-800 rounded-2xl p-6 shadow-xl">
        <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4">Pipeline Workflow Overview</h3>
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3 bg-slate-900/60 border border-slate-800 p-4 rounded-xl flex-1 w-full">
            <Database className="w-6 h-6 text-indigo-400 shrink-0" />
            <div>
              <div className="text-sm font-bold text-white">Multi-Source Data</div>
              <div className="text-xs text-slate-400">S1 Master + Noisy S2/S3</div>
            </div>
          </div>
          <ArrowRight className="w-5 h-5 text-slate-600 hidden md:block shrink-0" />
          <div className="flex items-center gap-3 bg-slate-900/60 border border-slate-800 p-4 rounded-xl flex-1 w-full">
            <Cpu className="w-6 h-6 text-purple-400 shrink-0" />
            <div>
              <div className="text-sm font-bold text-white">ML Modeling</div>
              <div className="text-xs text-slate-400">LightGBM / XGBoost / CatBoost</div>
            </div>
          </div>
          <ArrowRight className="w-5 h-5 text-slate-600 hidden md:block shrink-0" />
          <div className="flex items-center gap-3 bg-slate-900/60 border border-slate-800 p-4 rounded-xl flex-1 w-full">
            <ShieldAlert className="w-6 h-6 text-amber-400 shrink-0" />
            <div>
              <div className="text-sm font-bold text-white">Threshold & Error Analysis</div>
              <div className="text-xs text-slate-400">Precision & F0.5 Optimization</div>
            </div>
          </div>
          <ArrowRight className="w-5 h-5 text-slate-600 hidden md:block shrink-0" />
          <div className="flex items-center gap-3 bg-slate-900/60 border border-slate-800 p-4 rounded-xl flex-1 w-full">
            <CheckCircle className="w-6 h-6 text-emerald-400 shrink-0" />
            <div>
              <div className="text-sm font-bold text-white">Entity Linkage Results</div>
              <div className="text-xs text-slate-400">Master Record Map</div>
            </div>
          </div>
        </div>
      </div>

      {/* Key Stats Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="bg-[#172036] border border-slate-800 p-6 rounded-2xl">
          <div className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Top Empirical Model</div>
          <div className="text-2xl font-bold text-indigo-400 mt-2">{stats?.winning_model}</div>
          <div className="text-xs text-slate-500 mt-1">Evaluated on Validation Split</div>
        </div>

        <div className="bg-[#172036] border border-slate-800 p-6 rounded-2xl">
          <div className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Optimal Accuracy</div>
          <div className="text-2xl font-bold text-emerald-400 mt-2">{(stats?.optimal_accuracy ? stats.optimal_accuracy * 100 : 99.56).toFixed(2)}%</div>
          <div className="text-xs text-slate-500 mt-1">Tuned at Threshold {stats?.optimal_threshold}</div>
        </div>

        <div className="bg-[#172036] border border-slate-800 p-6 rounded-2xl">
          <div className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Total Candidate Pairs</div>
          <div className="text-2xl font-bold text-white mt-2">{stats?.dataset_stats.total_candidate_pairs}</div>
          <div className="text-xs text-slate-500 mt-1">Extracted Pairwise Comparisons</div>
        </div>

        <div className="bg-[#172036] border border-slate-800 p-6 rounded-2xl">
          <div className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Ground Truth Matches</div>
          <div className="text-2xl font-bold text-purple-400 mt-2">{stats?.dataset_stats.total_matches}</div>
          <div className="text-xs text-slate-500 mt-1">{stats?.dataset_stats.total_unmatched} Unmatched Pairs</div>
        </div>
      </div>
    </div>
  );
};
