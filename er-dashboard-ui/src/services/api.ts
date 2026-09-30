const API_BASE_URL = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8001/api';


export interface DashboardStats {
  project_name: string;
  winning_model: string;
  optimal_accuracy: number;
  optimal_threshold: number;
  dataset_stats: {
    s1_records: number;
    s2_records: number;
    s3_records: number;
    total_candidate_pairs: number;
    total_matches: number;
    total_unmatched: number;
  };
}

export interface DataOverview {
  datasets: Record<string, {
    record_count: number;
    columns: string[];
    missing_values: Record<string, number>;
    sample_records: any[];
  }>;
  features: {
    total_pairs: number;
    columns: string[];
    sample_features: any[];
  };
}

export interface ModelPerformance {
  selected_model: string;
  optimal_threshold: number;
  evaluation_strategy: string;
  comparison_table: Array<{
    model: string;
    accuracy_opt: number;
    precision_opt: number;
    recall_opt: number;
    f0_5_opt: number;
    f1_opt: number;
    pr_auc: number;
    optimal_threshold: number;
    fp_count: number;
    fn_count: number;
  }>;
}

export interface ErrorAnalysisData {
  optimal_threshold: number;
  total_false_positives: number;
  total_false_negatives: number;
  fp_categories: Array<{ category: string; count: number }>;
  fn_categories: Array<{ category: string; count: number }>;
  key_insights: string[];
}

export const fetchDashboardStats = async (): Promise<DashboardStats> => {
  const res = await fetch(`${API_BASE_URL}/dashboard/stats`);
  if (!res.ok) throw new Error("Failed to fetch dashboard stats");
  return res.json();
};

export const fetchDataOverview = async (): Promise<DataOverview> => {
  const res = await fetch(`${API_BASE_URL}/data/overview`);
  if (!res.ok) throw new Error("Failed to fetch data overview");
  return res.json();
};

export const fetchModelPerformance = async (): Promise<ModelPerformance> => {
  const res = await fetch(`${API_BASE_URL}/model/performance`);
  if (!res.ok) throw new Error("Failed to fetch model performance");
  return res.json();
};

export const fetchErrorAnalysis = async (): Promise<ErrorAnalysisData> => {
  const res = await fetch(`${API_BASE_URL}/error/analysis`);
  if (!res.ok) throw new Error("Failed to fetch error analysis");
  return res.json();
};

export const fetchResearchImprovement = async () => {
  const res = await fetch(`${API_BASE_URL}/research/improvement`);
  if (!res.ok) throw new Error("Failed to fetch research improvement data");
  return res.json();
};

export const searchCandidateEntities = async (query?: string) => {
  const url = query ? `${API_BASE_URL}/entity/search?query=${encodeURIComponent(query)}` : `${API_BASE_URL}/entity/search`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to search entities");
  return res.json();
};

export const fetchFinalResults = async () => {
  const res = await fetch(`${API_BASE_URL}/results/final`);
  if (!res.ok) throw new Error("Failed to fetch final linkage results");
  return res.json();
};
