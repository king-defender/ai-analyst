import { useState, useCallback } from 'react';
import { uploadDocument, isApiError } from '@/lib/api';
import { UploadResponse, ApiError } from '@/types/api';

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
    acceptedTypes = ['.pdf', '.txt', '.docx', '.json'],
    maxSize = 50 * 1024 * 1024 // 50MB default
  } = options;
  
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<ApiError | string | null>(null);
  const [uploadedFile, setUploadedFile] = useState<UploadResponse | null>(null);

  const validateFile = useCallback(async (file: File): Promise<string | null> => {
    // Check file size
    if (file.size > maxSize) {
      return `File size must be less than ${maxSize / 1024 / 1024}MB`;
    }

    // Check file type
    const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();
    if (!acceptedTypes.includes(fileExtension)) {
      return `File type not supported. Please upload: ${acceptedTypes.join(', ')}`;
    }

    // Additional JSON validation
    if (fileExtension === '.json') {
      try {
        const text = await file.text();
        JSON.parse(text);
      } catch (error) {
        return 'Invalid JSON file. Please ensure the file contains valid JSON data.';
      }
    }

    return null;
  }, [maxSize, acceptedTypes]);

  const uploadFile = useCallback(async (file: File) => {
    const validationError = await validateFile(file);
    if (validationError) {
      setError(validationError);
      onError?.(validationError);
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
  }, [onSuccess, onError, validateFile]);

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