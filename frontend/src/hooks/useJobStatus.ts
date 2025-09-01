import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api';
import { JobStatus } from '@/components/status/JobTracker';

interface UseJobStatusOptions {
  pollingInterval?: number;
  autoStart?: boolean;
}

export function useJobStatus(
  jobId: string | null,
  options: UseJobStatusOptions = {}
) {
  const { pollingInterval = 2000, autoStart = true } = options;
  
  const [status, setStatus] = useState<JobStatus | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isPolling, setIsPolling] = useState(false);

  const fetchStatus = async () => {
    if (!jobId) return;

    try {
      setLoading(true);
      setError(null);
      
      const response = await apiClient.getJobStatus(jobId);
      
      if (response.success) {
        setStatus(response.data);
      } else {
        setError(response.error || 'Failed to fetch job status');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  const startPolling = () => {
    setIsPolling(true);
  };

  const stopPolling = () => {
    setIsPolling(false);
  };

  useEffect(() => {
    if (!jobId || !autoStart) return;
    
    fetchStatus();
    startPolling();
  }, [jobId, autoStart]);

  useEffect(() => {
    if (!isPolling || !jobId) return;

    const interval = setInterval(fetchStatus, pollingInterval);
    
    return () => clearInterval(interval);
  }, [isPolling, jobId, pollingInterval]);

  // Stop polling when job is completed or failed
  useEffect(() => {
    if (status && ['completed', 'failed'].includes(status.status)) {
      stopPolling();
    }
  }, [status]);

  return {
    status,
    loading,
    error,
    isPolling,
    startPolling,
    stopPolling,
    refetch: fetchStatus,
  };
}