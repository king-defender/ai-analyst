'use client';

import { useState, useEffect } from 'react';
import FileUpload from '@/components/upload/FileUpload';
import JobTracker from '@/components/status/JobTracker';
import StartupDataDisplay from '@/components/data/StartupDataDisplay';
import BenchmarkDisplay from '@/components/benchmarks/BenchmarkDisplay';
import RiskDisplay from '@/components/risks/RiskDisplay';
import MemoViewer from '@/components/memo/MemoViewer';
import { useFileUpload } from '@/hooks/useFileUpload';
import { useJobStatus } from '@/hooks/useJobStatus';
import { apiClient } from '@/lib/api';
import { AnalysisResult } from '@/types/api';
import { downloadFile } from '@/utils/format';

type AnalysisStep = 'upload' | 'processing' | 'results';

export default function Home() {
  const [currentStep, setCurrentStep] = useState<AnalysisStep>('upload');
  const [jobId, setJobId] = useState<string | null>(null);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [activeTab, setActiveTab] = useState('data');

  const { uploadFile, uploading, error: uploadError } = useFileUpload({
    onSuccess: async (response) => {
      // Start analysis after successful upload
      const analysisResponse = await apiClient.startAnalysis(response.file_id);
      if (analysisResponse.success) {
        setJobId(analysisResponse.data.job_id);
        setCurrentStep('processing');
      }
    },
    onError: (error) => {
      console.error('Upload failed:', error);
    }
  });

  const { status } = useJobStatus(jobId, {
    autoStart: true,
  });

  // Handle analysis completion
  useEffect(() => {
    if (status?.status === 'completed' && status.result) {
      setAnalysisResult(status.result);
      setCurrentStep('results');
    }
  }, [status]);

  const handleExportPDF = async () => {
    if (!jobId) return;
    
    const pdfBlob = await apiClient.exportMemoPDF(jobId);
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
            <div className="text-center mb-8">
              <h1 className="text-4xl font-bold text-gray-900 mb-4">
                AI Analyst MVP
              </h1>
              <p className="text-xl text-gray-600 mb-8">
                Upload your pitch deck and get comprehensive analysis, benchmarking, and investor-ready deal memos.
              </p>
            </div>
            
            <FileUpload 
              onFileUpload={uploadFile}
              isUploading={uploading}
            />
            
            {uploadError && (
              <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-md">
                <p className="text-red-800">{uploadError}</p>
              </div>
            )}
            
            <div className="mt-12 max-w-md mx-auto bg-white rounded-lg shadow-sm border p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">How it works</h2>
              <ol className="space-y-3 text-gray-700">
                <li className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-medium">1</div>
                  <span>Upload your pitch deck (PDF, TXT, or DOCX)</span>
                </li>
                <li className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-medium">2</div>
                  <span>AI extracts key data and benchmarks against peers</span>
                </li>
                <li className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-medium">3</div>
                  <span>Risk assessment identifies potential concerns</span>
                </li>
                <li className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-medium">4</div>
                  <span>Generate and export investor-ready memo</span>
                </li>
              </ol>
            </div>
          </div>
        );
        
      case 'processing':
        return (
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-8">
              <h1 className="text-2xl font-bold text-gray-900 mb-2">
                Analyzing Your Pitch Deck
              </h1>
              <p className="text-gray-600">
                Our AI is processing your document and generating insights...
              </p>
            </div>
            
            {jobId && <JobTracker jobId={jobId} />}
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
                  companyName={analysisResult.startup_data.company_name}
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
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {renderContent()}
      </div>
    </div>
  );
}