import React, { useEffect, useState } from 'react';
import { fetchModelPerformance, ModelPerformance } from '../services/api';
import { Trophy, CheckCircle, BarChart2 } from 'lucide-react';

export const ModelPerformancePage: React.FC = () => {
  const [perf, setPerf] = useState<ModelPerformance | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetchModelPerformance()
      .then(res => {
        setPerf(res);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-8 text-indigo-400 animate-pulse">Loading model comparison matrix...</div>;

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold text-white">Empirical Model Comparison Matrix</h2>
        <p className="text-slate-400 mt-1">
          Supervised binary classification performance across gradient boosted trees evaluated on identical entity-level validation splits.
        </p>
      </div>

      {/* Winning Model Banner */}
      <div className="bg-gradient-to-r from-indigo-900/60 to-slate-900 border border-indigo-500/30 p-6 rounded-2xl flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-amber-500/20 border border-amber-500/40 flex items-center justify-center text-amber-400">
            <Trophy className="w-6 h-6" />
          </div>
          <div>
            <div className="text-xs font-semibold text-indigo-300 uppercase tracking-wider">Empirically Selected Champion</div>
            <div className="text-2xl font-bold text-white mt-0.5">{perf?.selected_model} Classifier</div>
            <div className="text-xs text-slate-400 mt-1">Leakage-Safe Strategy: {perf?.evaluation_strategy}</div>
          </div>
        </div>
        <div className="text-right">
          <div className="text-xs text-slate-400">Optimal Threshold</div>
          <div className="text-2xl font-bold text-emerald-400">{perf?.optimal_threshold}</div>
        </div>
      </div>

      {/* Model Matrix Table */}
      <div className="bg-[#172036] border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
        <div className="p-6 border-b border-slate-800 flex items-center justify-between">
          <h3 className="text-lg font-semibold text-white">Evaluation Comparison Matrix</h3>
          <span className="text-xs text-slate-400">Ranked by Validation Accuracy</span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-900/80 text-slate-400 uppercase text-xs font-semibold">
              <tr>
                <th className="p-4">Model</th>
                <th className="p-4 text-emerald-400">Accuracy (Opt)</th>
                <th className="p-4">Precision (Opt)</th>
                <th className="p-4">Recall (Opt)</th>
                <th className="p-4">F0.5 Score</th>
                <th className="p-4">F1 Score</th>
                <th className="p-4">PR-AUC</th>
                <th className="p-4">Opt Threshold</th>
                <th className="p-4">FP Count</th>
                <th className="p-4">FN Count</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {perf?.comparison_table.map((row, idx) => (
                <tr key={idx} className={row.model === perf.selected_model ? 'bg-indigo-600/10 font-medium' : 'hover:bg-slate-800/40'}>
                  <td className="p-4 font-bold text-white flex items-center gap-2">
                    {row.model === perf.selected_model && <CheckCircle className="w-4 h-4 text-emerald-400" />}
                    {row.model}
                  </td>
                  <td className="p-4 text-emerald-400 font-bold">{(row.accuracy_opt * 100).toFixed(2)}%</td>
                  <td className="p-4">{(row.precision_opt * 100).toFixed(2)}%</td>
                  <td className="p-4">{(row.recall_opt * 100).toFixed(2)}%</td>
                  <td className="p-4 font-semibold text-indigo-300">{row.f0_5_opt}</td>
                  <td className="p-4">{row.f1_opt}</td>
                  <td className="p-4 text-purple-300">{row.pr_auc}</td>
                  <td className="p-4 font-mono">{row.optimal_threshold}</td>
                  <td className="p-4 text-rose-400 font-semibold">{row.fp_count}</td>
                  <td className="p-4 text-amber-400 font-semibold">{row.fn_count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
