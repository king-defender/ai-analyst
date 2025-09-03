'use client';

import { useState } from 'react';
import { InvestorMemo } from '@/types/startup';
import { FileText, Download, Eye, Share2, Calendar, User } from 'lucide-react';

interface MemoViewerProps {
  memo: InvestorMemo;
  onExportPDF?: () => void;
}

export default function MemoViewer({ memo, onExportPDF }: MemoViewerProps) {
  const [activeSection, setActiveSection] = useState('executive_summary');

  const sections = [
    { key: 'executive_summary', label: 'Executive Summary', icon: Eye },
    { key: 'investment_thesis', label: 'Investment Thesis', icon: FileText },
    { key: 'market_analysis', label: 'Market Analysis', icon: FileText },
    { key: 'team_assessment', label: 'Team Assessment', icon: User },
    { key: 'financial_analysis', label: 'Financial Analysis', icon: FileText },
    { key: 'risk_analysis', label: 'Risk Analysis', icon: FileText },
    { key: 'recommendation', label: 'Recommendation', icon: FileText }
  ];

  const getRecommendationColor = (recommendation: string) => {
    switch (recommendation) {
      case 'strong_buy': return 'bg-green-100 text-green-800 border-green-200';
      case 'buy': return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'hold': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'pass': return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'strong_pass': return 'bg-red-100 text-red-800 border-red-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getRecommendationLabel = (recommendation: string) => {
    switch (recommendation) {
      case 'strong_buy': return 'Strong Buy';
      case 'buy': return 'Buy';
      case 'hold': return 'Hold';
      case 'pass': return 'Pass';
      case 'strong_pass': return 'Strong Pass';
      default: return recommendation;
    }
  };

  const formatCurrency = (amount: number) => {
    if (amount >= 1000000) {
      return `$${(amount / 1000000).toFixed(1)}M`;
    } else if (amount >= 1000) {
      return `$${(amount / 1000).toFixed(0)}K`;
    }
    return `$${amount.toLocaleString()}`;
  };

  const renderSection = () => {
    switch (activeSection) {
      case 'executive_summary':
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Company Overview</h3>
              <p className="text-gray-700 leading-relaxed">{memo.executive_summary.company_overview}</p>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Key Highlights</h3>
              <ul className="space-y-2">
                {memo.executive_summary.key_highlights.map((highlight, index) => (
                  <li key={index} className="flex items-start space-x-2">
                    <div className="w-2 h-2 bg-blue-600 rounded-full mt-2 flex-shrink-0" />
                    <span className="text-gray-700">{highlight}</span>
                  </li>
                ))}
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Investment Highlights</h3>
              <ul className="space-y-2">
                {memo.executive_summary.investment_highlights.map((highlight, index) => (
                  <li key={index} className="flex items-start space-x-2">
                    <div className="w-2 h-2 bg-green-600 rounded-full mt-2 flex-shrink-0" />
                    <span className="text-gray-700">{highlight}</span>
                  </li>
                ))}
              </ul>
            </div>
            
            {memo.executive_summary.concerns.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Key Concerns</h3>
                <ul className="space-y-2">
                  {memo.executive_summary.concerns.map((concern, index) => (
                    <li key={index} className="flex items-start space-x-2">
                      <div className="w-2 h-2 bg-red-600 rounded-full mt-2 flex-shrink-0" />
                      <span className="text-gray-700">{concern}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            
            <div className="bg-blue-50 p-4 rounded-lg">
              <h3 className="text-lg font-semibold text-blue-900 mb-2">Recommendation Summary</h3>
              <p className="text-blue-800">{memo.executive_summary.recommendation_summary}</p>
            </div>
          </div>
        );
        
      case 'investment_thesis':
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Value Proposition</h3>
              <p className="text-gray-700 leading-relaxed">{memo.investment_thesis.value_proposition}</p>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Market Opportunity</h3>
              <p className="text-gray-700 leading-relaxed">{memo.investment_thesis.market_opportunity}</p>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Competitive Advantages</h3>
              <ul className="space-y-2">
                {memo.investment_thesis.competitive_advantage.map((advantage, index) => (
                  <li key={index} className="flex items-start space-x-2">
                    <div className="w-2 h-2 bg-blue-600 rounded-full mt-2 flex-shrink-0" />
                    <span className="text-gray-700">{advantage}</span>
                  </li>
                ))}
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Growth Potential</h3>
              <p className="text-gray-700 leading-relaxed">{memo.investment_thesis.growth_potential}</p>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Exit Strategy</h3>
              <p className="text-gray-700 leading-relaxed">{memo.investment_thesis.exit_strategy}</p>
            </div>
          </div>
        );
        
      case 'recommendation':
        return (
          <div className="space-y-6">
            <div className="text-center">
              <div className={`inline-flex items-center px-6 py-3 rounded-full text-lg font-semibold border-2 ${getRecommendationColor(memo.recommendation.recommendation)}`}>
                {getRecommendationLabel(memo.recommendation.recommendation)}
              </div>
              
              <div className="mt-4">
                <p className="text-gray-600">Confidence Level</p>
                <p className="text-2xl font-bold text-gray-900">{(memo.recommendation.confidence_level * 100).toFixed(0)}%</p>
                <div className="w-32 bg-gray-200 rounded-full h-2 mx-auto mt-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${memo.recommendation.confidence_level * 100}%` }}
                  />
                </div>
              </div>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Reasoning</h3>
              <ul className="space-y-2">
                {memo.recommendation.reasoning.map((reason, index) => (
                  <li key={index} className="flex items-start space-x-2">
                    <div className="w-2 h-2 bg-blue-600 rounded-full mt-2 flex-shrink-0" />
                    <span className="text-gray-700">{reason}</span>
                  </li>
                ))}
              </ul>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-gray-50 p-4 rounded-lg">
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Valuation Range</h3>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Low:</span>
                    <span className="font-semibold">{formatCurrency(memo.recommendation.suggested_valuation_range.low)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">High:</span>
                    <span className="font-semibold">{formatCurrency(memo.recommendation.suggested_valuation_range.high)}</span>
                  </div>
                </div>
              </div>
              
              <div className="bg-gray-50 p-4 rounded-lg">
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Investment Suggestion</h3>
                <p className="text-2xl font-bold text-gray-900">
                  {formatCurrency(memo.recommendation.investment_amount_suggestion)}
                </p>
              </div>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Terms Suggestions</h3>
              <ul className="space-y-2">
                {memo.recommendation.terms_suggestions.map((term, index) => (
                  <li key={index} className="flex items-start space-x-2">
                    <div className="w-2 h-2 bg-blue-600 rounded-full mt-2 flex-shrink-0" />
                    <span className="text-gray-700">{term}</span>
                  </li>
                ))}
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Next Steps</h3>
              <ol className="space-y-2">
                {memo.recommendation.next_steps.map((step, index) => (
                  <li key={index} className="flex items-start space-x-3">
                    <div className="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-medium flex-shrink-0">
                      {index + 1}
                    </div>
                    <span className="text-gray-700">{step}</span>
                  </li>
                ))}
              </ol>
            </div>
          </div>
        );
        
      default:
        return (
          <div className="text-center text-gray-500 py-8">
            <FileText className="h-16 w-16 mx-auto mb-4" />
            <p>Select a section to view its content</p>
          </div>
        );
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border overflow-hidden">
      {/* Header */}
      <div className="border-b bg-gray-50 p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-gray-900 flex items-center">
            <FileText className="h-6 w-6 mr-2" />
            Investment Memo: {memo.company_name}
          </h2>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={onExportPDF}
              className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Download className="h-4 w-4" />
              <span>Export PDF</span>
            </button>
            
            <button className="flex items-center space-x-2 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors">
              <Share2 className="h-4 w-4" />
              <span>Share</span>
            </button>
          </div>
        </div>
        
        <div className="flex items-center text-sm text-gray-600">
          <Calendar className="h-4 w-4 mr-1" />
          <span>Generated on {new Date(memo.generated_at).toLocaleDateString()}</span>
        </div>
      </div>
      
      <div className="flex">
        {/* Sidebar Navigation */}
        <div className="w-64 border-r bg-gray-50 p-4">
          <nav className="space-y-1">
            {sections.map((section) => {
              const Icon = section.icon;
              return (
                <button
                  key={section.key}
                  onClick={() => setActiveSection(section.key)}
                  className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-left transition-colors ${
                    activeSection === section.key
                      ? 'bg-blue-100 text-blue-900 border border-blue-200'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span className="text-sm font-medium">{section.label}</span>
                </button>
              );
            })}
          </nav>
        </div>
        
        {/* Content Area */}
        <div className="flex-1 p-6">
          <div className="max-w-4xl">
            {renderSection()}
          </div>
        </div>
      </div>
    </div>
  );
}