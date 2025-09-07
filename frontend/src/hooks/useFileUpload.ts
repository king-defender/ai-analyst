import { useState, useCallback } from 'react';
import { uploadDocument, isApiError } from '@/lib/api';
import { UploadResponse, ApiError } from '@/types/api';
import { validateFile } from '@/utils/validation';

interface UseFileUploadOptions {
  onSuccess?: (response: UploadResponse) => void;
  onError?: (error: ApiError | string) => void;
  acceptedTypes?: string[];
  maxSize?: number; // in bytes
}

export function useFileUpload(options: UseFileUploadOptions = {}) {
  const { 
    onSuccess, 
    onError, 
    acceptedTypes = ['.pdf', '.txt', '.doc', '.docx', '.xls', '.xlsx', '.json'],
    maxSize = 50 * 1024 * 1024 // 50MB default
  } = options;
  
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<ApiError | string | null>(null);
  const [uploadedFile, setUploadedFile] = useState<UploadResponse | null>(null);

  const uploadFile = useCallback(async (file: File) => {
    const validationResult = await validateFile(file, acceptedTypes, maxSize);
    if (!validationResult.isValid) {
      setError(validationResult.error || 'Validation failed');
      onError?.(validationResult.error || 'Validation failed');
      return;
    }

    setUploading(true);
    setProgress(0);
    setError(null);
    setUploadedFile(null);

    try {
      // Simulate progress for better UX
      const progressInterval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return prev;
          }
          return prev + 10;
        });
      }, 200);

      const response = await uploadDocument(file);
      
      clearInterval(progressInterval);
      setProgress(100);

      setUploadedFile(response);
      onSuccess?.(response);
    } catch (err) {
      let errorToSet: ApiError | string;
      
      if (isApiError(err)) {
        // It's an ApiError
        errorToSet = err;
      } else if (err instanceof Error) {
        errorToSet = err.message;
      } else {
        errorToSet = 'Upload failed';
      }
      
      setError(errorToSet);
      onError?.(errorToSet);
    } finally {
      setUploading(false);
      setTimeout(() => setProgress(0), 1000);
    }
  }, [onSuccess, onError, acceptedTypes, maxSize]);

  const reset = useCallback(() => {
    setUploading(false);
    setProgress(0);
    setError(null);
    setUploadedFile(null);
  }, []);

  const retry = useCallback(() => {
    if (error && typeof error === 'object' && error.retryable) {
      setError(null);
      return true; // Indicate that retry is possible
    }
    return false;
  }, [error]);

  return {
    uploadFile,
    uploading,
    progress,
    error,
    uploadedFile,
    reset,
    retry,
  };
}