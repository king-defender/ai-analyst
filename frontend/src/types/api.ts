export interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
  error?: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}

export interface UploadResponse {
  job_id: string;
  file_id: string;
  filename: string;
  status: string;
}

export interface AnalysisResult {
  job_id: string;
  startup_data: import('./startup').StartupData;
  benchmark_data: import('./startup').BenchmarkData;
  risk_assessment: import('./startup').RiskAssessment;
  investor_memo: import('./startup').InvestorMemo;
  confidence_scores: {
    data_extraction: number;
    risk_assessment: number;
    benchmark_accuracy: number;
    memo_quality: number;
  };
}

export interface JobStatusResponse {
  id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  stage: string;
  progress?: number;
  message?: string;
  result?: AnalysisResult;
  error?: string;
  created_at: string;
  updated_at: string;
}

export interface ErrorResponse {
  error: string;
  details?: any;
  code?: string;
}