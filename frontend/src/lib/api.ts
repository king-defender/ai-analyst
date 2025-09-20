import { UploadResponse, JobStatusResponse, ApiError } from '@/types/api';
import { StartupData, InvestorMemo, BenchmarkData, RiskAssessment } from '@/types/startup';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Type guard to check if an error is an ApiError
 */
export function isApiError(error: unknown): error is ApiError {
  return (
    error !== null &&
    typeof error === 'object' &&
    'name' in error &&
    'message' in error &&
    'type' in error &&
    'status' in error &&
    'retryable' in error &&
    typeof (error as Record<string, unknown>).name === 'string' &&
    typeof (error as Record<string, unknown>).message === 'string' &&
    typeof (error as Record<string, unknown>).type === 'string' &&
    typeof (error as Record<string, unknown>).status === 'number' &&
    typeof (error as Record<string, unknown>).retryable === 'boolean'
  );
}

/**
 * Enhanced error handling with specific error types
 */
function createApiError(response: Response, errorData?: Record<string, unknown>): ApiError {
  const status = response.status;
  const statusText = response.statusText;
  
  // Categorize errors by status code
  switch (status) {
    case 429:
      return {
        name: 'RateLimitError',
        type: 'rate_limit',
        message: 'Too many requests. Please wait a moment before trying again.',
        status,
        retryAfter: response.headers.get('retry-after') || '60',
        retryable: true
      };
    case 413:
      return {
        name: 'FileTooLargeError',
        type: 'file_too_large',
        message: 'File size exceeds the maximum limit of 50MB.',
        status,
        retryable: false
      };
    case 415:
      return {
        name: 'UnsupportedFormatError',
        type: 'unsupported_format',
        message: 'File format not supported. Please upload PDF, TXT, DOCX, XLS, XLSX, or JSON files.',
        status,
        retryable: false
      };
    case 400:
      return {
        name: 'ValidationError',
        type: 'validation_error',
        message: (errorData?.detail as string) || (errorData?.error as string) || 'Invalid file or request.',
        status,
        retryable: false
      };
    case 500:
    case 502:
    case 503:
    case 504:
      return {
        name: 'ServerError',
        type: 'server_error',
        message: 'Server error occurred. Please try again in a few moments.',
        status,
        retryable: true
      };
    default:
      // Network errors or other issues
      if (status === 0 || !status) {
        return {
          name: 'NetworkError',
          type: 'network_error',
          message: 'Network connection failed. Please check your internet connection.',
          status: 0,
          retryable: true
        };
      }
      return {
        name: 'UnknownError',
        type: 'unknown_error',
        message: (errorData?.detail as string) || (errorData?.error as string) || `Upload failed (${status} ${statusText})`,
        status,
        retryable: true
      };
  }
}

/**
 * Upload a document file for analysis
 */
export async function uploadDocument(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch(`${API_BASE_URL}/api/documents/upload`, {
      method: 'POST',
      headers: {
        // Don't set Content-Type manually - let browser set it with boundary for multipart/form-data
      },
      body: formData,
      // Add credentials and CORS options for better compatibility
      credentials: 'include',
      mode: 'cors',
    });

    if (!response.ok) {
      let errorData;
      try {
        errorData = await response.json();
      } catch {
        // If response is not JSON (empty response), errorData will be undefined
        errorData = undefined;
      }
      const apiError = createApiError(response, errorData);
      throw apiError;
    }

    return response.json();
  } catch (error) {
    // Handle network errors (fetch failures, timeouts, etc.)
    if (error instanceof TypeError) {
      throw createApiError(new Response(null, { status: 0 }));
    }
    // Re-throw API errors as-is
    throw error;
  }
}

/**
 * Get the status of a processing job
 */
export async function getJobStatus(jobId: string): Promise<JobStatusResponse> {
  const response = await fetch(`${API_BASE_URL}/api/jobs/${jobId}/status`);

  if (!response.ok) {
    let errorData: Record<string, unknown> | undefined;
    try {
      errorData = await response.json();
    } catch (_) {
      errorData = undefined;
    }

    // Reuse the structured API error helper used elsewhere
    const apiError = createApiError(response, errorData);
    // Specialize 404 for callers that want to show a specific UX
    if (response.status === 404) {
      apiError.name = 'NotFoundError';
      apiError.retryable = false;
    }
    throw apiError;
  }

  return response.json();
}

/**
 * Export memo as PDF
 */
export async function exportMemoPDF(memoId: string): Promise<Blob> {
  const response = await fetch(`${API_BASE_URL}/api/memos/${memoId}/pdf`);

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ error: 'Failed to export PDF' }));
    throw new Error(errorData.detail || errorData.error || 'Failed to export PDF');
  }

  return response.blob();
}

/**
 * Get extracted data from a document
 */
export async function getExtractedData(documentId: string): Promise<StartupData> {
  const response = await fetch(`${API_BASE_URL}/api/documents/${documentId}/extracted-data`);

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ error: 'Failed to get extracted data' }));
    throw new Error(errorData.detail || errorData.error || 'Failed to get extracted data');
  }

  return response.json();
}

/**
 * Generate an investment memo from analysis results
 */
export async function generateMemo(fileId: string): Promise<InvestorMemo> {
  const response = await fetch(`${API_BASE_URL}/api/memos/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ file_id: fileId }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ error: 'Failed to generate memo' }));
    throw new Error(errorData.detail || errorData.error || 'Failed to generate memo');
  }

  return response.json();
}

/**
 * Get benchmark data for a file
 */
export async function getBenchmarkData(fileId: string): Promise<BenchmarkData> {
  const response = await fetch(`${API_BASE_URL}/api/analysis/${fileId}/benchmarks`);

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ error: 'Failed to get benchmark data' }));
    throw new Error(errorData.detail || errorData.error || 'Failed to get benchmark data');
  }

  return response.json();
}

/**
 * Get risk assessment for a file
 */
export async function getRiskAssessment(fileId: string): Promise<RiskAssessment> {
  const response = await fetch(`${API_BASE_URL}/api/analysis/${fileId}/risks`);

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ error: 'Failed to get risk assessment' }));
    throw new Error(errorData.detail || errorData.error || 'Failed to get risk assessment');
  }

  return response.json();
}

// Convenience wrapper for tests and consumers that prefer an object API
export const apiClient = {
  uploadDocument,
  getJobStatus,
  exportMemoPDF,
  getExtractedData,
  generateMemo,
  getBenchmarkData,
  getRiskAssessment,
};
