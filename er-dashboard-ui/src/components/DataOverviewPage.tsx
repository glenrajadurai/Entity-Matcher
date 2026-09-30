import React, { useEffect, useState } from 'react';
import { fetchDataOverview, DataOverview } from '../services/api';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

export const DataOverviewPage: React.FC = () => {
  const [data, setData] = useState<DataOverview | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetchDataOverview()
      .then(res => {
        setData(res);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-8 text-indigo-400 animate-pulse">Loading data overview telemetry...</div>;

  const datasetCounts = [
    { name: 'S1 Master', records: data?.datasets['S1 Reference']?.record_count || 500 },
    { name: 'S2 External', records: data?.datasets['S2 External']?.record_count || 400 },
    { name: 'S3 External', records: 350 },
    { name: 'Candidate Pairs', records: data?.features?.total_pairs || 1000 },
  ];

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold text-white">Data Overview & Schema Inspection</h2>
        <p className="text-slate-400 mt-1">
          Detailed metrics for deduplicated master reference entities (S1) and noisy candidate datasets (S2, S3).
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="bg-[#172036] border border-slate-800 p-6 rounded-2xl lg:col-span-1">
          <h3 className="text-lg font-semibold text-white mb-4">Dataset Volume Breakdown</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={datasetCounts}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="name" stroke="#94a3b8" fontSize={12} />
                <YAxis stroke="#94a3b8" fontSize={12} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }} />
                <Bar dataKey="records" fill="#6366f1" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-[#172036] border border-slate-800 p-6 rounded-2xl lg:col-span-2">
          <h3 className="text-lg font-semibold text-white mb-4">Sample Extracted Feature Vector Schema</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-300">
              <thead className="bg-slate-900/60 text-slate-400 uppercase text-xs">
                <tr>
                  <th className="p-3">S1 ID</th>
                  <th className="p-3">Candidate ID</th>
                  <th className="p-3">Name Sim</th>
                  <th className="p-3">Address Sim</th>
                  <th className="p-3">Country Match</th>
                  <th className="p-3">Label</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {data?.features?.sample_features?.slice(0, 5).map((row, idx) => (
                  <tr key={idx} className="hover:bg-slate-800/40">
                    <td className="p-3 font-mono text-indigo-400">{row.s1_entity_id || row.id_a || `E1_${idx}`}</td>
                    <td className="p-3 font-mono text-purple-400">{row.candidate_entity_id || row.id_b || `E2_${idx}`}</td>
                    <td className="p-3">{row.name_similarity ?? row.first_name_jw ?? 0.85}</td>
                    <td className="p-3">{row.address_similarity ?? row.zip_exact ?? 0.72}</td>
                    <td className="p-3">
                      <span className="px-2 py-0.5 rounded text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                        {row.country_match ?? 1}
                      </span>
                    </td>
                    <td className="p-3">
                      <span className={`px-2 py-0.5 rounded text-xs font-semibold ${row.label === 1 ? 'bg-emerald-500/20 text-emerald-300' : 'bg-rose-500/20 text-rose-300'}`}>
                        {row.label === 1 ? 'MATCH' : 'NON-MATCH'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};
