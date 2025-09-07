'use client';

import { useState, useEffect } from 'react';
import { CheckCircle, Clock, AlertCircle, Loader2 } from 'lucide-react';
import { JobStatusResponse } from '@/types/api';

interface JobTrackerProps {
  jobId: string;
  onStatusChange?: (status: JobStatusResponse) => void;
}

const stages = [
  { key: 'upload', label: 'File Upload', description: 'Processing uploaded file' },
  { key: 'ocr', label: 'Text Extraction', description: 'Extracting text from document' },
  { key: 'parsing', label: 'Data Parsing', description: 'Analyzing startup information' },
  { key: 'benchmark', label: 'Benchmarking', description: 'Comparing against peers' },
  { key: 'risks', label: 'Risk Assessment', description: 'Identifying potential risks' },
  { key: 'memo', label: 'Memo Generation', description: 'Creating investor memo' }
];

export default function JobTracker({ jobId, onStatusChange }: JobTrackerProps) {
  const [jobStatus, setJobStatus] = useState<JobStatusResponse | null>(null);
  const [currentStageIndex, setCurrentStageIndex] = useState(0);

  useEffect(() => {
    if (!jobId) return;

    let stopped = false;
    let attempts = 0;
    const maxAttempts = 30; // e.g., poll every 2s for 1 minute

    const pollStatus = async () => {
      try {
        attempts++;
        const response = await fetch(`/api/jobs/${jobId}/status`);
        if (response.status === 404) {
          setJobStatus(null);
          if (attempts >= maxAttempts) {
            stopped = true;
            alert('Job not found. Please try uploading again.');
          }
          return;
        }
        const status: JobStatusResponse = await response.json();
        setJobStatus(status);
        onStatusChange?.(status);

        // Update current stage based on status
        const stageIndex = stages.findIndex(stage => stage.key === status.stage);
        if (stageIndex >= 0) {
          setCurrentStageIndex(stageIndex);
        }
        if (status.status === 'completed' || status.status === 'failed') {
          stopped = true;
        }
      } catch (error) {
        console.error('Error polling job status:', error);
      }
    };

    // Poll every 2 seconds
    const interval = setInterval(() => {
      if (!stopped) pollStatus();
    }, 2000);
    pollStatus(); // Initial call

    return () => clearInterval(interval);
  }, [jobId, onStatusChange]);

  if (!jobStatus) {
    // Only show error if polling actually received a 404 (not just initial state)
    const handleReset = () => {
      window.location.reload();
    };
    return (
      <div className="flex flex-col items-center justify-center p-8">
        <div className="flex items-center mb-2">
          <AlertCircle className="h-8 w-8 text-red-500 mr-2" />
          <span className="text-red-600 font-semibold">Job not found or expired.</span>
        </div>
        <ul className="mb-4 text-sm text-red-500 list-disc list-inside">
          <li>The job may have expired due to backend restart (MVP uses in-memory jobs).</li>
          <li>The job ID may be invalid or the file was never uploaded.</li>
          <li>If you restarted the backend, all jobs are lost. Please re-upload your file.</li>
          <li>If this persists, check backend logs for errors or contact support.</li>
        </ul>
        <button
          onClick={handleReset}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
        >
          Reset & Upload New File
        </button>
      </div>
    );
  }

  // Show job progress and results if jobStatus exists
  if (jobStatus) {
    return (
      <div className="w-full max-w-2xl mx-auto">
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold">Job Status: {jobStatus.status}</h2>
            <div>Stage: {jobStatus.stage}</div>
          </div>
          {typeof jobStatus.progress === 'number' && (
            <div className="mb-2">Progress: {jobStatus.progress}%</div>
          )}
          {jobStatus.message && (
            <div className="mb-2">Message: {jobStatus.message}</div>
          )}
          {jobStatus.status === 'completed' && jobStatus.result && (
            <div className="mt-4 p-4 bg-gray-100 rounded">
              <h3 className="font-semibold mb-2">AI Analysis Result</h3>
              <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>{JSON.stringify(jobStatus.result, null, 2)}</pre>
            </div>
          )}
          {jobStatus.status === 'failed' && jobStatus.error && (
            <div className="mt-4 p-4 bg-red-100 rounded text-red-700">
              <h3 className="font-semibold mb-2">Error</h3>
              <pre>{jobStatus.error}</pre>
            </div>
          )}
        </div>
      </div>
    );
  }

  // unreachable code removed
}