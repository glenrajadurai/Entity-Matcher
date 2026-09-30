import React from 'react';
import { ArrowDown, Layers, Server, Cpu, Database, CheckCircle2 } from 'lucide-react';

export const ArchitecturePage: React.FC = () => {
  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold text-white">System Architecture & API Integration</h2>
        <p className="text-slate-400 mt-1">
          High-level overview demonstrating real-time communication between React Frontend and FastAPI Backend.
        </p>
      </div>

      <div className="max-w-xl mx-auto space-y-4">
        {/* Layer 1: React Frontend */}
        <div className="bg-[#172036] border border-indigo-500/40 p-6 rounded-2xl flex items-center justify-between shadow-lg shadow-indigo-500/10">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-indigo-500/20 text-indigo-400 flex items-center justify-center font-bold">
              <Layers className="w-6 h-6" />
            </div>
            <div>
              <div className="font-bold text-white text-lg">React + TypeScript Frontend</div>
              <div className="text-xs text-slate-400">Vite + Tailwind CSS + Recharts UI</div>
            </div>
          </div>
          <span className="text-xs px-2.5 py-1 bg-indigo-500/20 text-indigo-300 rounded font-mono">Port 5173</span>
        </div>

        <div className="flex justify-center">
          <ArrowDown className="w-6 h-6 text-indigo-400 animate-bounce" />
        </div>

        {/* Layer 2: FastAPI Backend */}
        <div className="bg-[#172036] border border-purple-500/40 p-6 rounded-2xl flex items-center justify-between shadow-lg shadow-purple-500/10">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-purple-500/20 text-purple-400 flex items-center justify-center font-bold">
              <Server className="w-6 h-6" />
            </div>
            <div>
              <div className="font-bold text-white text-lg">Python FastAPI Backend</div>
              <div className="text-xs text-slate-400">Centralized REST API (`src/services/api.ts`)</div>
            </div>
          </div>
          <span className="text-xs px-2.5 py-1 bg-purple-500/20 text-purple-300 rounded font-mono">Port 8001</span>
        </div>

        <div className="flex justify-center">
          <ArrowDown className="w-6 h-6 text-purple-400 animate-bounce" />
        </div>

        {/* Layer 3: ML Model & Data */}
        <div className="bg-[#172036] border border-emerald-500/40 p-6 rounded-2xl flex items-center justify-between shadow-lg shadow-emerald-500/10">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold">
              <Cpu className="w-6 h-6" />
            </div>
            <div>
              <div className="font-bold text-white text-lg">Empirical ML Model & Pipeline</div>
              <div className="text-xs text-slate-400">LightGBM Classifier + Group K-Fold Data Splitter</div>
            </div>
          </div>
          <span className="text-xs px-2.5 py-1 bg-emerald-500/20 text-emerald-300 rounded font-mono">Joblib Serialized</span>
        </div>
      </div>
    </div>
  );
};
