import React from 'react';
import { Sparkles, Clock, GitCompare } from 'lucide-react';

export const ResearchImprovementPage: React.FC = () => {
  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold text-white">Research Improvement Handoff</h2>
        <p className="text-slate-400 mt-1">
          Collaborative research direction combining Member 1 (data noise), Member 2 (blocking), and Member 3 (ML modeling).
        </p>
      </div>

      <div className="bg-[#172036] border border-slate-800 p-6 rounded-2xl">
        <div className="flex items-center gap-3 text-amber-400 font-semibold mb-2">
          <Clock className="w-5 h-5" />
          <h3>Research Results Status: In Progress</h3>
        </div>
        <p className="text-sm text-slate-300">
          Baseline model (LightGBM) achieves <strong className="text-emerald-400">99.56% Validation Accuracy</strong>. Team research improvements are currently pending joint integration across all three members.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-[#172036] border border-slate-800 p-6 rounded-2xl">
          <div className="flex items-center gap-2 text-indigo-400 font-semibold mb-4">
            <GitCompare className="w-5 h-5" />
            <h3>Baseline Model Strategy</h3>
          </div>
          <div className="space-y-2 text-sm text-slate-300">
            <div>• Champion Model: LightGBM Gradient Booster</div>
            <div>• Optimal Decision Threshold: 0.05</div>
            <div>• Splitting Strategy: GroupShuffleSplit (Entity-Level)</div>
          </div>
        </div>

        <div className="bg-[#172036] border border-slate-800 p-6 rounded-2xl">
          <div className="flex items-center gap-2 text-emerald-400 font-semibold mb-4">
            <Sparkles className="w-5 h-5" />
            <h3>Proposed Research Enhancements</h3>
          </div>
          <div className="space-y-2 text-sm text-slate-300">
            <div>• Member 1: Soft-Jaccard tokenization on noisy addresses</div>
            <div>• Member 2: Location-aware multi-pass blocking rules</div>
            <div>• Member 3: Transformer embedding re-ranking on hard negatives</div>
          </div>
        </div>
      </div>
    </div>
  );
};
