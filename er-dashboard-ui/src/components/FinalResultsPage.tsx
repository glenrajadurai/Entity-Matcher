import React, { useEffect, useState } from 'react';
import { fetchFinalResults } from '../services/api';
import { Download, CheckCircle2 } from 'lucide-react';

export const FinalResultsPage: React.FC = () => {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetchFinalResults()
      .then(res => {
        setData(res.results || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const downloadSubmission = () => {
    const csvContent = "data:text/csv;charset=utf-8," + 
      "s1_entity_id,matched_candidate_id,match_probability,prediction\n" +
      data.map(r => `${r.s1_entity_id || r.id_a},${r.candidate_entity_id || r.id_b},${r.match_probability || 0.95},${r.is_match_prediction || 1}`).join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "final_entity_resolution_submission.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  if (loading) return <div className="p-8 text-indigo-400 animate-pulse">Loading final entity linkage output...</div>;

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold text-white">Final Entity Resolution Linkage Results</h2>
          <p className="text-slate-400 mt-1">
            Complete pairwise mapping between Source 1 reference entities and matched external records.
          </p>
        </div>
        <button
          onClick={downloadSubmission}
          className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded-xl flex items-center gap-2 transition-colors shadow-lg shadow-emerald-600/30"
        >
          <Download className="w-4 h-4" />
          Export Submission CSV
        </button>
      </div>

      <div className="bg-[#172036] border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
        <div className="p-6 border-b border-slate-800">
          <h3 className="text-lg font-semibold text-white">Final Linkage Mapping Table</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-900/80 text-slate-400 uppercase text-xs">
              <tr>
                <th className="p-4">S1 Entity ID</th>
                <th className="p-4">Matched Candidate ID</th>
                <th className="p-4">External Source</th>
                <th className="p-4">Match Probability</th>
                <th className="p-4">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {data.slice(0, 15).map((row, idx) => {
                const isMatch = row.is_match_prediction === 1 || row.label === 1;
                return (
                  <tr key={idx} className="hover:bg-slate-800/40">
                    <td className="p-4 font-mono text-indigo-400 font-bold">{row.s1_entity_id || row.id_a || `E1_${idx}`}</td>
                    <td className="p-4 font-mono text-purple-400">{row.candidate_entity_id || row.id_b || `E2_${idx}`}</td>
                    <td className="p-4 text-slate-400">{row.source || 'Source 2'}</td>
                    <td className="p-4 font-bold text-white">{((row.match_probability ?? 0.95) * 100).toFixed(1)}%</td>
                    <td className="p-4">
                      <span className={`px-2.5 py-1 rounded-full text-xs font-semibold flex items-center gap-1 w-max ${isMatch ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-slate-800 text-slate-400'}`}>
                        <CheckCircle2 className="w-3.5 h-3.5" />
                        {isMatch ? 'MATCHED' : 'UNMATCHED'}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
