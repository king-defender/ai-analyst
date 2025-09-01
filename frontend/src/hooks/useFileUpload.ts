import { useState, useCallback } from 'react';
import { apiClient } from '@/lib/api';
import { UploadResponse } from '@/types/api';

interface UseFileUploadOptions {
  onSuccess?: (response: UploadResponse) => void;
  onError?: (error: string) => void;
  acceptedTypes?: string[];
  maxSize?: number; // in bytes
}

export function useFileUpload(options: UseFileUploadOptions = {}) {
  const { 
    onSuccess, 
    onError, 
    acceptedTypes = ['.pdf', '.txt', '.docx'],
    maxSize = 50 * 1024 * 1024 // 50MB default
  } = options;
  
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [uploadedFile, setUploadedFile] = useState<UploadResponse | null>(null);

  const validateFile = (file: File): string | null => {
    // Check file size
    if (file.size > maxSize) {
      return `File size must be less than ${maxSize / 1024 / 1024}MB`;
    }

    // Check file type
    const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();
    if (!acceptedTypes.includes(fileExtension)) {
      return `File type not supported. Please upload: ${acceptedTypes.join(', ')}`;
    }

    return null;
  };

  const uploadFile = useCallback(async (file: File) => {
    const validationError = validateFile(file);
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

      const response = await apiClient.uploadFile(file);
      
      clearInterval(progressInterval);
      setProgress(100);

      if (response.success) {
        setUploadedFile(response.data);
        onSuccess?.(response.data);
      } else {
        const errorMessage = response.error || 'Upload failed';
        setError(errorMessage);
        onError?.(errorMessage);
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Upload failed';
      setError(errorMessage);
      onError?.(errorMessage);
    } finally {
      setUploading(false);
      setTimeout(() => setProgress(0), 1000);
    }
  }, [maxSize, acceptedTypes, onSuccess, onError]);

  const reset = useCallback(() => {
    setUploading(false);
    setProgress(0);
    setError(null);
    setUploadedFile(null);
  }, []);

  return {
    uploadFile,
    uploading,
    progress,
    error,
    uploadedFile,
    reset,
  };
}