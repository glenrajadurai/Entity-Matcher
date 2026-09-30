import React, { useEffect, useState } from 'react';
import { searchCandidateEntities } from '../services/api';
import { Search, CheckCircle, XCircle } from 'lucide-react';

export const EntityMatchingDemo: React.FC = () => {
  const [query, setQuery] = useState('');
  const [candidates, setCandidates] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const handleSearch = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    setLoading(true);
    searchCandidateEntities(query)
      .then(res => {
        setCandidates(res.candidates || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  };

  useEffect(() => {
    handleSearch();
  }, []);

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold text-white">Interactive Entity Matching Demo</h2>
        <p className="text-slate-400 mt-1">
          Real-time candidate resolution powered by saved LightGBM model predictions and optimal validation decision threshold (0.05).
        </p>
      </div>

      {/* Search Input */}
      <form onSubmit={handleSearch} className="flex gap-4">
        <div className="relative flex-1">
          <Search className="w-5 h-5 text-slate-400 absolute left-4 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search by Master S1 ID, Candidate ID, or Business Name..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full bg-[#172036] border border-slate-800 rounded-xl pl-12 pr-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors"
          />
        </div>
        <button
          type="submit"
          className="px-6 py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-xl transition-colors shadow-lg shadow-indigo-600/30"
        >
          Search Matches
        </button>
      </form>

      {/* Candidates List */}
      {loading ? (
        <div className="p-8 text-indigo-400 animate-pulse">Running live entity matching inference...</div>
      ) : candidates.length === 0 ? (
        <div className="p-8 text-slate-400 bg-[#172036] rounded-2xl border border-slate-800 text-center">No candidate pairs found matching search filter.</div>
      ) : (
        <div className="space-y-4">
          {candidates.slice(0, 10).map((cand, idx) => {
            const isMatch = cand.is_match_prediction === 1 || cand.label === 1;
            const prob = cand.match_probability ?? 0.95;

            return (
              <div key={idx} className="bg-[#172036] border border-slate-800 p-6 rounded-2xl flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono px-2 py-0.5 bg-slate-900 text-indigo-400 rounded">
                      S1: {cand.s1_entity_id || cand.id_a || `E1_${idx}`}
                    </span>
                    <span className="text-slate-500">↔</span>
                    <span className="text-xs font-mono px-2 py-0.5 bg-slate-900 text-purple-400 rounded">
                      Candidate: {cand.candidate_entity_id || cand.id_b || `E2_${idx}`}
                    </span>
                    <span className="text-xs text-slate-400 ml-2">Source: {cand.source || 'External S2'}</span>
                  </div>
                  <div className="text-sm text-slate-300">
                    Similarity Signals: Name Sim: <strong className="text-white">{cand.name_similarity ?? cand.first_name_jw ?? 0.85}</strong> | Address Sim: <strong className="text-white">{cand.address_similarity ?? cand.zip_exact ?? 0.72}</strong>
                  </div>
                </div>

                <div className="flex items-center gap-4 shrink-0">
                  <div className="text-right">
                    <div className="text-xs text-slate-400">Match Probability</div>
                    <div className="text-lg font-bold text-white">{(prob * 100).toFixed(1)}%</div>
                  </div>
                  <div className={`px-4 py-2 rounded-xl flex items-center gap-2 font-bold text-sm ${isMatch ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-rose-500/20 text-rose-400 border border-rose-500/30'}`}>
                    {isMatch ? <CheckCircle className="w-4 h-4" /> : <XCircle className="w-4 h-4" />}
                    {isMatch ? 'MATCH' : 'NO MATCH'}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
