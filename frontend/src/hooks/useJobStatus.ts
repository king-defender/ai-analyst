import { useState, useEffect, useCallback } from 'react';
import { getJobStatus } from '@/lib/api';
import { JobStatusResponse } from '@/types/api';

interface UseJobStatusOptions {
  pollingInterval?: number;
  autoStart?: boolean;
}

export function useJobStatus(
  jobId: string | null,
  options: UseJobStatusOptions = {}
) {
  const { pollingInterval = 2000, autoStart = true } = options;
  
  const [status, setStatus] = useState<JobStatusResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isPolling, setIsPolling] = useState(false);

  const fetchStatus = useCallback(async () => {
    if (!jobId) return;

    try {
      setLoading(true);
      setError(null);
      
      const response = await getJobStatus(jobId);
      
      setStatus(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  }, [jobId]);

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
  }, [jobId, autoStart, fetchStatus]);

  useEffect(() => {
    if (!isPolling || !jobId) return;

    const interval = setInterval(fetchStatus, pollingInterval);
    
    return () => clearInterval(interval);
  }, [isPolling, jobId, pollingInterval, fetchStatus]);

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