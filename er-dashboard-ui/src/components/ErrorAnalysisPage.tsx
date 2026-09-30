import React, { useEffect, useState } from 'react';
import { fetchErrorAnalysis, ErrorAnalysisData } from '../services/api';
import { AlertCircle, FileWarning, Lightbulb } from 'lucide-react';

export const ErrorAnalysisPage: React.FC = () => {
  const [data, setData] = useState<ErrorAnalysisData | null>(null);

  useEffect(() => {
    fetchErrorAnalysis().then(res => setData(res)).catch(() => {});
  }, []);

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold text-white">Error Analysis Taxonomy</h2>
        <p className="text-slate-400 mt-1">
          Detailed breakdown of prediction failures (False Positives and False Negatives) analyzed at optimal threshold {data?.optimal_threshold || 0.05}.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-[#172036] border border-slate-800 p-6 rounded-2xl">
          <div className="flex items-center gap-3 text-rose-400 font-semibold mb-4">
            <AlertCircle className="w-5 h-5" />
            <h3>False Positives (Incorrect Matches)</h3>
          </div>
          <div className="text-3xl font-bold text-white mb-4">{data?.total_false_positives || 0}</div>
          <p className="text-xs text-slate-400">
            Records incorrectly classified as entity matches when they refer to different businesses.
          </p>
        </div>

        <div className="bg-[#172036] border border-slate-800 p-6 rounded-2xl">
          <div className="flex items-center gap-3 text-amber-400 font-semibold mb-4">
            <FileWarning className="w-5 h-5" />
            <h3>False Negatives (Missed Matches)</h3>
          </div>
          <div className="text-3xl font-bold text-white mb-4">{data?.total_false_negatives || 1}</div>
          <p className="text-xs text-slate-400">
            True matching entity records missed due to string noise, typos, or address conflicts.
          </p>
        </div>
      </div>

      {/* Failure Mode Recommendations */}
      <div className="bg-[#172036] border border-slate-800 p-6 rounded-2xl">
        <div className="flex items-center gap-3 text-indigo-400 font-semibold mb-4">
          <Lightbulb className="w-5 h-5" />
          <h3>Handoff Insights for Team Research</h3>
        </div>
        <ul className="space-y-3">
          {data?.key_insights.map((insight, idx) => (
            <li key={idx} className="flex items-start gap-3 bg-slate-900/60 p-4 rounded-xl border border-slate-800">
              <span className="text-xs font-bold px-2 py-1 bg-indigo-500/20 text-indigo-300 rounded shrink-0">{idx + 1}</span>
              <span className="text-sm text-slate-300">{insight}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};
