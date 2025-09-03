'use client';

import { useState, useEffect } from 'react';
import { CheckCircle, Clock, AlertCircle, Loader2 } from 'lucide-react';

export interface JobStatus {
  id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  stage: string;
  progress?: number;
  message?: string;
  created_at: string;
  updated_at: string;
  result?: any;
}

interface JobTrackerProps {
  jobId: string;
  onStatusChange?: (status: JobStatus) => void;
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
  const [jobStatus, setJobStatus] = useState<JobStatus | null>(null);
  const [currentStageIndex, setCurrentStageIndex] = useState(0);

  useEffect(() => {
    if (!jobId) return;

    const pollStatus = async () => {
      try {
        const response = await fetch(`/api/jobs/${jobId}/status`);
        const status: JobStatus = await response.json();
        
        setJobStatus(status);
        onStatusChange?.(status);

        // Update current stage based on status
        const stageIndex = stages.findIndex(stage => stage.key === status.stage);
        if (stageIndex >= 0) {
          setCurrentStageIndex(stageIndex);
        }
      } catch (error) {
        console.error('Error polling job status:', error);
      }
    };

    // Poll every 2 seconds
    const interval = setInterval(pollStatus, 2000);
    pollStatus(); // Initial call

    return () => clearInterval(interval);
  }, [jobId, onStatusChange]);

  if (!jobStatus) {
    return (
      <div className="flex items-center justify-center p-8">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
        <span className="ml-2 text-gray-600">Loading job status...</span>
      </div>
    );
  }

  const getStageIcon = (index: number) => {
    if (index < currentStageIndex) {
      return <CheckCircle className="h-5 w-5 text-green-500" />;
    } else if (index === currentStageIndex) {
      if (jobStatus.status === 'failed') {
        return <AlertCircle className="h-5 w-5 text-red-500" />;
      }
      return <Loader2 className="h-5 w-5 animate-spin text-blue-600" />;
    } else {
      return <Clock className="h-5 w-5 text-gray-400" />;
    }
  };

  const getStageStatus = (index: number) => {
    if (index < currentStageIndex) return 'completed';
    if (index === currentStageIndex) {
      if (jobStatus.status === 'failed') return 'failed';
      return 'processing';
    }
    return 'pending';
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-gray-900">Analysis Progress</h3>
          <span className={`px-3 py-1 rounded-full text-sm font-medium ${
            jobStatus.status === 'completed' ? 'bg-green-100 text-green-800' :
            jobStatus.status === 'failed' ? 'bg-red-100 text-red-800' :
            'bg-blue-100 text-blue-800'
          }`}>
            {jobStatus.status}
          </span>
        </div>

        <div className="space-y-4">
          {stages.map((stage, index) => {
            const status = getStageStatus(index);
            
            return (
              <div key={stage.key} className="flex items-start space-x-3">
                <div className="flex-shrink-0 mt-1">
                  {getStageIcon(index)}
                </div>
                
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <p className={`text-sm font-medium ${
                      status === 'completed' ? 'text-green-900' :
                      status === 'processing' ? 'text-blue-900' :
                      status === 'failed' ? 'text-red-900' :
                      'text-gray-500'
                    }`}>
                      {stage.label}
                    </p>
                    
                    {index === currentStageIndex && jobStatus.progress && (
                      <span className="text-sm text-gray-600">
                        {jobStatus.progress}%
                      </span>
                    )}
                  </div>
                  
                  <p className="text-sm text-gray-600">
                    {index === currentStageIndex && jobStatus.message 
                      ? jobStatus.message 
                      : stage.description
                    }
                  </p>

                  {index === currentStageIndex && jobStatus.progress && (
                    <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${jobStatus.progress}%` }}
                      />
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {jobStatus.status === 'failed' && (
          <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-md">
            <div className="flex">
              <AlertCircle className="h-5 w-5 text-red-400" />
              <div className="ml-3">
                <h4 className="text-sm font-medium text-red-800">Analysis Failed</h4>
                <p className="mt-1 text-sm text-red-700">
                  {jobStatus.message || 'An error occurred during processing. Please try again.'}
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}