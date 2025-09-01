'use client';

import { StartupData } from '@/types/startup';
import { Building, Users, Calendar, DollarSign, TrendingUp, MapPin } from 'lucide-react';

interface StartupDataDisplayProps {
  data: StartupData;
}

export default function StartupDataDisplay({ data }: StartupDataDisplayProps) {
  const formatCurrency = (amount: number) => {
    if (amount >= 1000000) {
      return `$${(amount / 1000000).toFixed(1)}M`;
    } else if (amount >= 1000) {
      return `$${(amount / 1000).toFixed(0)}K`;
    }
    return `$${amount.toLocaleString()}`;
  };

  const formatPercentage = (value: number) => `${(value * 100).toFixed(1)}%`;

  return (
    <div className="space-y-6">
      {/* Company Overview */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <Building className="h-5 w-5 mr-2" />
          Company Overview
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="text-sm font-medium text-gray-500">Company Name</label>
            <p className="text-lg font-semibold text-gray-900">{data.company_name}</p>
          </div>
          
          <div>
            <label className="text-sm font-medium text-gray-500">Founded</label>
            <p className="text-gray-900">{data.founded_year}</p>
          </div>
          
          <div>
            <label className="text-sm font-medium text-gray-500">Industry</label>
            <p className="text-gray-900">{data.industry}</p>
          </div>
          
          <div>
            <label className="text-sm font-medium text-gray-500">Stage</label>
            <p className="text-gray-900">{data.stage}</p>
          </div>
        </div>
        
        <div className="mt-4">
          <label className="text-sm font-medium text-gray-500">Description</label>
          <p className="text-gray-700 mt-1">{data.description}</p>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <TrendingUp className="h-5 w-5 mr-2" />
          Key Metrics
        </h3>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {data.metrics.revenue_arr && (
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <p className="text-2xl font-bold text-blue-900">
                {formatCurrency(data.metrics.revenue_arr)}
              </p>
              <p className="text-sm text-blue-600">ARR</p>
            </div>
          )}
          
          {data.metrics.monthly_growth_rate && (
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <p className="text-2xl font-bold text-green-900">
                {formatPercentage(data.metrics.monthly_growth_rate)}
              </p>
              <p className="text-sm text-green-600">Monthly Growth</p>
            </div>
          )}
          
          {data.metrics.customer_count && (
            <div className="text-center p-4 bg-purple-50 rounded-lg">
              <p className="text-2xl font-bold text-purple-900">
                {data.metrics.customer_count.toLocaleString()}
              </p>
              <p className="text-sm text-purple-600">Customers</p>
            </div>
          )}
          
          {data.metrics.runway_months && (
            <div className="text-center p-4 bg-orange-50 rounded-lg">
              <p className="text-2xl font-bold text-orange-900">
                {data.metrics.runway_months}
              </p>
              <p className="text-sm text-orange-600">Months Runway</p>
            </div>
          )}
        </div>
      </div>

      {/* Team */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <Users className="h-5 w-5 mr-2" />
          Team ({data.team.length} members)
        </h3>
        
        <div className="space-y-4">
          {data.team.slice(0, 5).map((member, index) => (
            <div key={index} className="flex items-start space-x-4 p-4 bg-gray-50 rounded-lg">
              <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center">
                <span className="text-white font-semibold">
                  {member.name.split(' ').map(n => n[0]).join('')}
                </span>
              </div>
              
              <div className="flex-1">
                <h4 className="font-semibold text-gray-900">{member.name}</h4>
                <p className="text-sm text-blue-600">{member.role}</p>
                <p className="text-sm text-gray-600 mt-1">{member.bio}</p>
                
                {member.previous_companies && member.previous_companies.length > 0 && (
                  <div className="mt-2">
                    <p className="text-xs text-gray-500">Previous: {member.previous_companies.join(', ')}</p>
                  </div>
                )}
              </div>
              
              <div className="text-right">
                <p className="text-sm font-medium text-gray-900">{member.experience_years} years</p>
                <p className="text-xs text-gray-500">experience</p>
              </div>
            </div>
          ))}
          
          {data.team.length > 5 && (
            <p className="text-center text-gray-500 text-sm">
              +{data.team.length - 5} more team members
            </p>
          )}
        </div>
      </div>

      {/* Financial Data */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <DollarSign className="h-5 w-5 mr-2" />
          Financial Information
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-gray-900 mb-3">Funding</h4>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-gray-600">Total Raised:</span>
                <span className="font-medium">{formatCurrency(data.financial_data.total_funding_raised)}</span>
              </div>
              
              {data.financial_data.current_valuation && (
                <div className="flex justify-between">
                  <span className="text-gray-600">Valuation:</span>
                  <span className="font-medium">{formatCurrency(data.financial_data.current_valuation)}</span>
                </div>
              )}
              
              {data.financial_data.last_funding_amount && (
                <div className="flex justify-between">
                  <span className="text-gray-600">Last Round:</span>
                  <span className="font-medium">{formatCurrency(data.financial_data.last_funding_amount)}</span>
                </div>
              )}
            </div>
          </div>
          
          <div>
            <h4 className="font-medium text-gray-900 mb-3">Unit Economics</h4>
            <div className="space-y-2">
              {data.financial_data.unit_economics.cac && (
                <div className="flex justify-between">
                  <span className="text-gray-600">CAC:</span>
                  <span className="font-medium">{formatCurrency(data.financial_data.unit_economics.cac)}</span>
                </div>
              )}
              
              {data.financial_data.unit_economics.ltv && (
                <div className="flex justify-between">
                  <span className="text-gray-600">LTV:</span>
                  <span className="font-medium">{formatCurrency(data.financial_data.unit_economics.ltv)}</span>
                </div>
              )}
              
              {data.financial_data.unit_economics.payback_period_months && (
                <div className="flex justify-between">
                  <span className="text-gray-600">Payback Period:</span>
                  <span className="font-medium">{data.financial_data.unit_economics.payback_period_months} months</span>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Product & Market */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Product</h3>
          
          <div className="space-y-3">
            <div>
              <label className="text-sm font-medium text-gray-500">Product Name</label>
              <p className="text-gray-900">{data.product_info.product_name}</p>
            </div>
            
            <div>
              <label className="text-sm font-medium text-gray-500">Type</label>
              <p className="text-gray-900">{data.product_info.product_type}</p>
            </div>
            
            <div>
              <label className="text-sm font-medium text-gray-500">Development Stage</label>
              <p className="text-gray-900">{data.product_info.development_stage}</p>
            </div>
            
            <div>
              <label className="text-sm font-medium text-gray-500">Key Features</label>
              <ul className="list-disc list-inside text-gray-700 text-sm mt-1 space-y-1">
                {data.product_info.key_features.slice(0, 3).map((feature, index) => (
                  <li key={index}>{feature}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <MapPin className="h-5 w-5 mr-2" />
            Market
          </h3>
          
          <div className="space-y-3">
            <div>
              <label className="text-sm font-medium text-gray-500">TAM</label>
              <p className="text-gray-900">{formatCurrency(data.market_data.total_addressable_market)}</p>
            </div>
            
            <div>
              <label className="text-sm font-medium text-gray-500">SAM</label>
              <p className="text-gray-900">{formatCurrency(data.market_data.serviceable_addressable_market)}</p>
            </div>
            
            <div>
              <label className="text-sm font-medium text-gray-500">Growth Rate</label>
              <p className="text-gray-900">{formatPercentage(data.market_data.market_growth_rate)}</p>
            </div>
            
            <div>
              <label className="text-sm font-medium text-gray-500">Position</label>
              <p className="text-gray-900">{data.market_data.market_position}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}