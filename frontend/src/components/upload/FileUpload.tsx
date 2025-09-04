'use client';

import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, AlertCircle, CheckCircle } from 'lucide-react';

interface FileUploadProps {
  onFileUpload: (file: File) => void;
  isUploading?: boolean;
  uploadProgress?: number;
  acceptedTypes?: string[];
  uploadStatus?: 'idle' | 'uploading' | 'success' | 'error';
  error?: string | null;
}

export default function FileUpload({ 
  onFileUpload, 
  isUploading = false,
  uploadProgress = 0,
  acceptedTypes = ['.pdf', '.txt', '.docx'],
  uploadStatus = 'idle',
  error: externalError
}: FileUploadProps) {
  const [internalError, setInternalError] = useState<string | null>(null);
  
  const displayError = externalError || internalError;

  const onDrop = useCallback((acceptedFiles: File[], fileRejections: { errors: { code: string }[] }[]) => {
    setInternalError(null);
    
    if (fileRejections.length > 0) {
      const rejection = fileRejections[0];
      if (rejection.errors.some((e) => e.code === 'file-invalid-type')) {
        setInternalError('Please upload a valid PDF, TXT, or DOCX file');
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
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
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
        return {
          title: 'Upload failed',
          subtitle: 'Please try again'
        };
      default:
        return {
          title: isDragActive ? 'Drop your file here' : 'Upload your pitch deck',
          subtitle: isDragActive ? 'Release to upload' : 'Drag & drop or click to select'
        };
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
        <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md flex items-center space-x-2">
          <AlertCircle className="h-5 w-5 text-red-500 flex-shrink-0" />
          <span className="text-red-700">{displayError}</span>
        </div>
      )}
    </div>
  );
}