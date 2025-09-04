import { UploadResponse, JobStatusResponse } from '@/types/api';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Upload a document file for analysis
 */
export async function uploadDocument(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append('file', file);

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
      // If response is not JSON (empty response), provide a fallback
      errorData = { 
        error: response.status === 429 ? 'Rate limit exceeded. Please try again in a moment.' : 'Upload failed',
        status: response.status
      };
    }
    throw new Error(errorData.detail || errorData.error || `Upload failed (${response.status})`);
  }

  return response.json();
}

/**
 * Get the status of a processing job
 */
export async function getJobStatus(jobId: string): Promise<JobStatusResponse> {
  const response = await fetch(`${API_BASE_URL}/api/jobs/${jobId}/status`);

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ error: 'Failed to get job status' }));
    throw new Error(errorData.detail || errorData.error || 'Failed to get job status');
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
export async function getExtractedData(documentId: string): Promise<any> {
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
export async function generateMemo(fileId: string): Promise<any> {
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
export async function getBenchmarkData(fileId: string): Promise<any> {
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
export async function getRiskAssessment(fileId: string): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/api/analysis/${fileId}/risks`);

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ error: 'Failed to get risk assessment' }));
    throw new Error(errorData.detail || errorData.error || 'Failed to get risk assessment');
  }

  return response.json();
}