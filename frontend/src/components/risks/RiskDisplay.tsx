'use client';

import { RiskAssessment, RiskFactor, RedFlag, YellowFlag } from '@/types/startup';
import { AlertTriangle, AlertCircle, Shield, TrendingDown, ExclamationTriangle } from 'lucide-react';

interface RiskDisplayProps {
  riskAssessment: RiskAssessment;
  companyName: string;
}

export default function RiskDisplay({ riskAssessment, companyName }: RiskDisplayProps) {
  const getRiskScoreColor = (score: number) => {
    if (score >= 80) return 'text-red-600 bg-red-100';
    if (score >= 60) return 'text-orange-600 bg-orange-100';
    if (score >= 40) return 'text-yellow-600 bg-yellow-100';
    return 'text-green-600 bg-green-100';
  };

  const getRiskScoreLabel = (score: number) => {
    if (score >= 80) return 'High Risk';
    if (score >= 60) return 'Medium-High Risk';
    if (score >= 40) return 'Medium Risk';
    return 'Low Risk';
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'bg-red-100 text-red-800 border-red-200';
      case 'high': return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'market': return <TrendingDown className="h-4 w-4" />;
      case 'financial': return <ExclamationTriangle className="h-4 w-4" />;
      case 'team': return <AlertCircle className="h-4 w-4" />;
      case 'product': return <Shield className="h-4 w-4" />;
      case 'competitive': return <AlertTriangle className="h-4 w-4" />;
      case 'regulatory': return <ExclamationTriangle className="h-4 w-4" />;
      default: return <AlertCircle className="h-4 w-4" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Overall Risk Score */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center">
            <Shield className="h-5 w-5 mr-2" />
            Risk Assessment
          </h3>
          
          <div className={`px-4 py-2 rounded-full font-semibold ${getRiskScoreColor(riskAssessment.overall_risk_score)}`}>
            {riskAssessment.overall_risk_score}/100 - {getRiskScoreLabel(riskAssessment.overall_risk_score)}
          </div>
        </div>
        
        <div className="w-full bg-gray-200 rounded-full h-3">
          <div 
            className={`h-3 rounded-full transition-all duration-300 ${
              riskAssessment.overall_risk_score >= 80 ? 'bg-red-500' :
              riskAssessment.overall_risk_score >= 60 ? 'bg-orange-500' :
              riskAssessment.overall_risk_score >= 40 ? 'bg-yellow-500' :
              'bg-green-500'
            }`}
            style={{ width: `${riskAssessment.overall_risk_score}%` }}
          />
        </div>
      </div>

      {/* Red Flags */}
      {riskAssessment.red_flags.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h3 className="text-lg font-semibold text-red-900 mb-4 flex items-center">
            <AlertTriangle className="h-5 w-5 mr-2 text-red-600" />
            Red Flags ({riskAssessment.red_flags.length})
          </h3>
          
          <div className="space-y-4">
            {riskAssessment.red_flags.map((flag, index) => (
              <div key={index} className="border-l-4 border-red-500 bg-red-50 p-4 rounded-r-lg">
                <div className="flex items-start justify-between mb-2">
                  <h4 className="font-semibold text-red-900">{flag.type}</h4>
                  <span className="bg-red-100 text-red-800 px-2 py-1 rounded text-sm font-medium">
                    Severity: {flag.severity_score}/10
                  </span>
                </div>
                
                <p className="text-red-800 mb-3">{flag.description}</p>
                
                {flag.evidence.length > 0 && (
                  <div className="mb-3">
                    <p className="text-red-700 font-medium text-sm mb-1">Evidence:</p>
                    <ul className="list-disc list-inside text-red-700 text-sm space-y-1">
                      {flag.evidence.map((evidence, evidenceIndex) => (
                        <li key={evidenceIndex}>{evidence}</li>
                      ))}
                    </ul>
                  </div>
                )}
                
                <div className="bg-red-100 p-3 rounded">
                  <p className="text-red-800 font-medium text-sm mb-1">Recommendation:</p>
                  <p className="text-red-800 text-sm">{flag.recommendation}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Yellow Flags */}
      {riskAssessment.yellow_flags.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h3 className="text-lg font-semibold text-yellow-900 mb-4 flex items-center">
            <AlertCircle className="h-5 w-5 mr-2 text-yellow-600" />
            Yellow Flags ({riskAssessment.yellow_flags.length})
          </h3>
          
          <div className="space-y-4">
            {riskAssessment.yellow_flags.map((flag, index) => (
              <div key={index} className="border-l-4 border-yellow-500 bg-yellow-50 p-4 rounded-r-lg">
                <h4 className="font-semibold text-yellow-900 mb-2">{flag.type}</h4>
                <p className="text-yellow-800 mb-3">{flag.description}</p>
                
                {flag.evidence.length > 0 && (
                  <div className="mb-3">
                    <p className="text-yellow-700 font-medium text-sm mb-1">Evidence:</p>
                    <ul className="list-disc list-inside text-yellow-700 text-sm space-y-1">
                      {flag.evidence.map((evidence, evidenceIndex) => (
                        <li key={evidenceIndex}>{evidence}</li>
                      ))}
                    </ul>
                  </div>
                )}
                
                <div className="bg-yellow-100 p-3 rounded">
                  <p className="text-yellow-800 font-medium text-sm mb-1">Monitoring Suggestion:</p>
                  <p className="text-yellow-800 text-sm">{flag.monitoring_suggestion}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Risk Factors by Category */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Risk Factors by Category</h3>
        
        <div className="space-y-4">
          {['market', 'team', 'financial', 'product', 'competitive', 'regulatory'].map(category => {
            const categoryRisks = riskAssessment.risk_factors.filter(risk => risk.category === category);
            
            if (categoryRisks.length === 0) return null;
            
            return (
              <div key={category} className="border rounded-lg p-4">
                <h4 className="font-semibold text-gray-900 mb-3 flex items-center capitalize">
                  {getCategoryIcon(category)}
                  <span className="ml-2">{category} Risks ({categoryRisks.length})</span>
                </h4>
                
                <div className="space-y-3">
                  {categoryRisks.map((risk, index) => (
                    <div key={index} className={`border rounded-lg p-3 ${getSeverityColor(risk.severity)}`}>
                      <div className="flex items-start justify-between mb-2">
                        <h5 className="font-medium">{risk.risk_type}</h5>
                        <span className="text-xs font-medium uppercase">
                          {risk.severity}
                        </span>
                      </div>
                      
                      <p className="text-sm mb-2">{risk.description}</p>
                      
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
                        <div>
                          <span className="font-medium">Likelihood:</span> {(risk.likelihood * 100).toFixed(0)}%
                        </div>
                        <div>
                          <span className="font-medium">Impact:</span> {risk.potential_impact}/10
                        </div>
                      </div>
                      
                      {risk.evidence.length > 0 && (
                        <div className="mt-2">
                          <p className="font-medium text-xs mb-1">Evidence:</p>
                          <ul className="list-disc list-inside text-xs space-y-1">
                            {risk.evidence.slice(0, 2).map((evidence, evidenceIndex) => (
                              <li key={evidenceIndex}>{evidence}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Risk Mitigation Suggestions */}
      {riskAssessment.risk_mitigation_suggestions.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <Shield className="h-5 w-5 mr-2" />
            Risk Mitigation Strategies
          </h3>
          
          <div className="space-y-3">
            {riskAssessment.risk_mitigation_suggestions.map((suggestion, index) => (
              <div key={index} className="flex items-start space-x-3 p-3 bg-blue-50 rounded-lg">
                <div className="flex-shrink-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-medium">
                  {index + 1}
                </div>
                <p className="text-blue-900">{suggestion}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}