'use client';

import { useState, useEffect } from 'react';
import { AlertCircle } from 'lucide-react';
import FileUpload from '@/components/upload/FileUpload';
import JobTracker from '@/components/status/JobTracker';
import StartupDataDisplay from '@/components/data/StartupDataDisplay';
import BenchmarkDisplay from '@/components/benchmarks/BenchmarkDisplay';
import RiskDisplay from '@/components/risks/RiskDisplay';
import MemoViewer from '@/components/memo/MemoViewer';
import { useFileUpload } from '@/hooks/useFileUpload';
import { useJobStatus } from '@/hooks/useJobStatus';
import { exportMemoPDF } from '@/lib/api';
import { AnalysisResult } from '@/types/api';
import { downloadFile } from '@/utils/format';

type AnalysisStep = 'upload' | 'processing' | 'results';

export default function Home() {
  const [currentStep, setCurrentStep] = useState<AnalysisStep>('upload');
  const [jobId, setJobId] = useState<string | null>(null);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [activeTab, setActiveTab] = useState('data');
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');

  const { uploadFile, uploading, progress, error: uploadError } = useFileUpload({
    onSuccess: async (response) => {
      setUploadStatus('success');
      // Response contains job_id directly from upload
      setJobId(response.job_id);
      setTimeout(() => {
        setCurrentStep('processing');
      }, 1000); // Brief delay to show success state
    },
    onError: (error) => {
      console.error('Upload failed:', error);
      setUploadStatus('error');
      setTimeout(() => setUploadStatus('idle'), 3000); // Reset after 3 seconds
    }
  });

  const { status } = useJobStatus(jobId, {
    autoStart: true,
  });

  // Handle file upload
  const handleFileUpload = (file: File) => {
    setUploadStatus('uploading');
    uploadFile(file);
  };

  // Handle analysis completion
  useEffect(() => {
    if (status?.status === 'completed' && status.result) {
      setAnalysisResult(status.result);
      setCurrentStep('results');
    }
  }, [status]);

  const handleExportPDF = async () => {
    if (!jobId) return;
    
    const pdfBlob = await exportMemoPDF(jobId);
    if (pdfBlob) {
      const filename = `${analysisResult?.startup_data.company_name || 'startup'}-memo.pdf`;
      downloadFile(pdfBlob, filename);
    }
  };

  const renderContent = () => {
    switch (currentStep) {
      case 'upload':
        return (
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-12">
              <h1 className="text-5xl font-bold text-gray-900 mb-6 leading-tight">
                AI Analyst MVP
              </h1>
              <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto leading-relaxed">
                Upload your pitch deck and get comprehensive analysis, benchmarking, and investor-ready deal memos powered by advanced AI.
              </p>
            </div>
            
            <div className="mb-12">
              <FileUpload 
                onFileUpload={handleFileUpload}
                isUploading={uploading}
                uploadProgress={progress}
                uploadStatus={uploadStatus}
                error={uploadError}
              />
            </div>
            
            {uploadError && uploadStatus === 'error' && (
              <div className="mb-8 p-4 bg-red-50 border border-red-200 rounded-lg shadow-sm">
                <div className="flex items-center space-x-3">
                  <AlertCircle className="h-5 w-5 text-red-500 flex-shrink-0" />
                  <div>
                    <p className="text-red-800 font-medium">Upload Failed</p>
                    <p className="text-red-700 text-sm">{uploadError}</p>
                  </div>
                </div>
              </div>
            )}
            
            <div className="max-w-lg mx-auto bg-white rounded-xl shadow-lg border p-8">
              <h2 className="text-xl font-semibold text-gray-900 mb-6 text-center">How it works</h2>
              <ol className="space-y-4 text-gray-700">
                <li className="flex items-start space-x-4">
                  <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-semibold flex-shrink-0">1</div>
                  <div>
                    <p className="font-medium">Upload your pitch deck</p>
                    <p className="text-sm text-gray-500">(PDF, TXT, or DOCX)</p>
                  </div>
                </li>
                <li className="flex items-start space-x-4">
                  <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-semibold flex-shrink-0">2</div>
                  <div>
                    <p className="font-medium">AI extracts key data</p>
                    <p className="text-sm text-gray-500">Benchmarks against industry peers</p>
                  </div>
                </li>
                <li className="flex items-start space-x-4">
                  <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-semibold flex-shrink-0">3</div>
                  <div>
                    <p className="font-medium">Risk assessment</p>
                    <p className="text-sm text-gray-500">Identifies potential concerns</p>
                  </div>
                </li>
                <li className="flex items-start space-x-4">
                  <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-semibold flex-shrink-0">4</div>
                  <div>
                    <p className="font-medium">Generate investor memo</p>
                    <p className="text-sm text-gray-500">Export ready-to-share analysis</p>
                  </div>
                </li>
              </ol>
            </div>
          </div>
        );
        
      case 'processing':
        return (
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-12">
              <h1 className="text-3xl font-bold text-gray-900 mb-4">
                Analyzing Your Pitch Deck
              </h1>
              <p className="text-lg text-gray-600 mb-8">
                Our AI is processing your document and generating comprehensive insights...
              </p>
            </div>
            
            <div className="bg-white rounded-xl shadow-lg border p-8">
              {jobId && <JobTracker jobId={jobId} />}
            </div>
          </div>
        );
        
      case 'results':
        if (!analysisResult) return null;
        
        return (
          <div className="max-w-7xl mx-auto">
            <div className="mb-8">
              <div className="flex items-center justify-between mb-4">
                <h1 className="text-2xl font-bold text-gray-900">
                  Analysis Results: {analysisResult.startup_data.company_name}
                </h1>
                
                <button
                  onClick={handleExportPDF}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Export Full Memo
                </button>
              </div>
              
              {/* Tab Navigation */}
              <div className="border-b border-gray-200">
                <nav className="-mb-px flex space-x-8">
                  {[
                    { key: 'data', label: 'Company Data' },
                    { key: 'benchmarks', label: 'Benchmarks' },
                    { key: 'risks', label: 'Risk Assessment' },
                    { key: 'memo', label: 'Investor Memo' }
                  ].map((tab) => (
                    <button
                      key={tab.key}
                      onClick={() => setActiveTab(tab.key)}
                      className={`py-2 px-1 border-b-2 font-medium text-sm ${
                        activeTab === tab.key
                          ? 'border-blue-500 text-blue-600'
                          : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                      }`}
                    >
                      {tab.label}
                    </button>
                  ))}
                </nav>
              </div>
            </div>
            
            {/* Tab Content */}
            <div className="mt-6">
              {activeTab === 'data' && (
                <StartupDataDisplay data={analysisResult.startup_data} />
              )}
              
              {activeTab === 'benchmarks' && (
                <BenchmarkDisplay 
                  data={analysisResult.benchmark_data}
                  companyName={analysisResult.startup_data.company_name}
                />
              )}
              
              {activeTab === 'risks' && (
                <RiskDisplay 
                  riskAssessment={analysisResult.risk_assessment}
                />
              )}
              
              {activeTab === 'memo' && (
                <MemoViewer 
                  memo={analysisResult.investor_memo}
                  onExportPDF={handleExportPDF}
                />
              )}
            </div>
          </div>
        );
        
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen">
      <div className="container mx-auto px-4 py-8">
        {renderContent()}
      </div>
    </div>
  );
}