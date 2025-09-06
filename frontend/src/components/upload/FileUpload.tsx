'use client';

import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, AlertCircle, CheckCircle, RefreshCw, Clock, WifiOff } from 'lucide-react';
import { ApiError } from '@/types/api';

interface FileUploadProps {
  onFileUpload: (file: File) => void;
  isUploading?: boolean;
  uploadProgress?: number;
  acceptedTypes?: string[];
  uploadStatus?: 'idle' | 'uploading' | 'success' | 'error';
  error?: ApiError | string | null;
  onRetry?: () => void;
}

export default function FileUpload({ 
  onFileUpload, 
  isUploading = false,
  uploadProgress = 0,
  acceptedTypes = ['.pdf', '.txt', '.doc', '.docx', '.xls', '.xlsx', '.json'],
  uploadStatus = 'idle',
  error: externalError,
  onRetry
}: FileUploadProps) {
  const [internalError, setInternalError] = useState<string | null>(null);
  
  const displayError = externalError || internalError;

  const onDrop = useCallback((acceptedFiles: File[], fileRejections: { errors: { code: string }[] }[]) => {
    setInternalError(null);
    
    if (fileRejections.length > 0) {
      const rejection = fileRejections[0];
      if (rejection.errors.some((e) => e.code === 'file-invalid-type')) {
        setInternalError('Please upload a valid PDF, TXT, DOC, DOCX, XLS, XLSX, or JSON file');
      } else if (rejection.errors.some((e) => e.code === 'file-too-large')) {
        setInternalError('File size is too large. Maximum size is 50MB');
      } else {
        setInternalError('File upload failed. Please try again');
      }
      return;
    }

    if (acceptedFiles.length > 0) {
      onFileUpload(acceptedFiles[0]);
    }
  }, [onFileUpload]);

  const { getRootProps, getInputProps, isDragActive, open } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'text/plain': ['.txt'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/msword': ['.doc'],
      'application/vnd.ms-excel': ['.xls'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/json': ['.json']
    },
    maxFiles: 1,
    maxSize: 50 * 1024 * 1024, // 50MB
    disabled: isUploading,
    noClick: true, // We'll handle clicks manually
    noKeyboard: true
  });

  const getStatusIcon = () => {
    switch (uploadStatus) {
      case 'uploading':
        return <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>;
      case 'success':
        return <CheckCircle className="h-12 w-12 text-green-500" />;
      case 'error':
        // Show different icons based on error type
        if (displayError && typeof displayError === 'object') {
          switch (displayError.type) {
            case 'network_error':
              return <WifiOff className="h-12 w-12 text-red-500" />;
            case 'rate_limit':
              return <Clock className="h-12 w-12 text-orange-500" />;
            default:
              return <AlertCircle className="h-12 w-12 text-red-500" />;
          }
        }
        return <AlertCircle className="h-12 w-12 text-red-500" />;
      default:
        return <Upload className="h-12 w-12 text-gray-400" />;
    }
  };

  const getStatusText = () => {
    switch (uploadStatus) {
      case 'uploading':
        return {
          title: 'Uploading...',
          subtitle: uploadProgress > 0 ? `${uploadProgress}% complete` : 'Processing your file'
        };
      case 'success':
        return {
          title: 'Upload successful!',
          subtitle: 'Your file is being processed'
        };
      case 'error':
        if (displayError && typeof displayError === 'object') {
          return {
            title: getErrorTitle(displayError.type),
            subtitle: displayError.message
          };
        }
        return {
          title: 'Upload failed',
          subtitle: typeof displayError === 'string' ? displayError : 'Please try again'
        };
      default:
        return {
          title: isDragActive ? 'Drop your file here' : 'Upload your pitch deck',
          subtitle: isDragActive ? 'Release to upload' : 'Drag & drop or click to select'
        };
    }
  };

  const getErrorTitle = (errorType: string) => {
    switch (errorType) {
      case 'rate_limit':
        return 'Rate limit exceeded';
      case 'network_error':
        return 'Connection failed';
      case 'file_too_large':
        return 'File too large';
      case 'unsupported_format':
        return 'Unsupported format';
      case 'server_error':
        return 'Server error';
      default:
        return 'Upload failed';
    }
  };

  const statusText = getStatusText();

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all duration-200
          ${isDragActive ? 'border-blue-500 bg-blue-50 scale-105' : 'border-gray-300 hover:border-gray-400'}
          ${isUploading ? 'opacity-75 cursor-not-allowed' : 'hover:shadow-md'}
          ${uploadStatus === 'success' ? 'border-green-300 bg-green-50' : ''}
          ${uploadStatus === 'error' || displayError ? 'border-red-300 bg-red-50' : ''}
        `}
        onClick={!isUploading ? open : undefined}
      >
        <input {...getInputProps()} />
        
        <div className="flex flex-col items-center space-y-4">
          {getStatusIcon()}
          
          <div>
            <p className={`text-lg font-medium ${
              uploadStatus === 'success' ? 'text-green-900' : 
              uploadStatus === 'error' || displayError ? 'text-red-900' : 'text-gray-900'
            }`}>
              {statusText.title}
            </p>
            <p className={`text-sm mt-1 ${
              uploadStatus === 'success' ? 'text-green-600' : 
              uploadStatus === 'error' || displayError ? 'text-red-600' : 'text-gray-500'
            }`}>
              {statusText.subtitle}
            </p>
          </div>
          
          {uploadProgress > 0 && uploadStatus === 'uploading' && (
            <div className="w-full max-w-xs">
              <div className="bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${Math.min(uploadProgress, 100)}%` }}
                ></div>
              </div>
            </div>
          )}
          
          <div className="flex items-center space-x-2 text-sm text-gray-500">
            <FileText className="h-4 w-4" />
            <span>Supports: {acceptedTypes.join(', ')}</span>
          </div>
        </div>
      </div>

      {displayError && (
        <div className={`mt-4 p-4 rounded-lg border flex flex-col space-y-3 ${
          displayError && typeof displayError === 'object' && displayError.type === 'rate_limit' 
            ? 'bg-orange-50 border-orange-200' 
            : 'bg-red-50 border-red-200'
        }`}>
          <div className="flex items-center space-x-2">
            {displayError && typeof displayError === 'object' ? (
              <>
                {displayError.type === 'network_error' && <WifiOff className="h-5 w-5 text-red-500 flex-shrink-0" />}
                {displayError.type === 'rate_limit' && <Clock className="h-5 w-5 text-orange-500 flex-shrink-0" />}
                {displayError.type === 'server_error' && <AlertCircle className="h-5 w-5 text-red-500 flex-shrink-0" />}
                {!['network_error', 'rate_limit', 'server_error'].includes(displayError.type) && <AlertCircle className="h-5 w-5 text-red-500 flex-shrink-0" />}
                <div className="flex-1">
                  <p className={`font-medium ${
                    displayError.type === 'rate_limit' ? 'text-orange-800' : 'text-red-800'
                  }`}>
                    {getErrorTitle(displayError.type)}
                  </p>
                  <p className={`text-sm ${
                    displayError.type === 'rate_limit' ? 'text-orange-700' : 'text-red-700'
                  }`}>
                    {displayError.message}
                  </p>
                  {displayError.retryAfter && (
                    <p className="text-xs text-orange-600 mt-1">
                      Please wait {displayError.retryAfter} seconds before retrying.
                    </p>
                  )}
                </div>
              </>
            ) : (
              <>
                <AlertCircle className="h-5 w-5 text-red-500 flex-shrink-0" />
                <span className="text-red-700">{displayError}</span>
              </>
            )}
          </div>
          
          {/* Retry button for retryable errors */}
          {displayError && typeof displayError === 'object' && displayError.retryable && onRetry && (
            <button
              onClick={onRetry}
              disabled={isUploading}
              className="self-start flex items-center space-x-2 px-3 py-2 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <RefreshCw className="h-4 w-4" />
              <span>Try Again</span>
            </button>
          )}
        </div>
      )}
    </div>
  );
}