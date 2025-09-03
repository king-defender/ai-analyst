'use client';

import { BenchmarkData } from '@/types/startup';
import { BarChart, TrendingUp, Target, Users } from 'lucide-react';

interface BenchmarkDisplayProps {
  data: BenchmarkData;
  companyName: string;
}

export default function BenchmarkDisplay({ data, companyName }: BenchmarkDisplayProps) {
  const formatCurrency = (amount: number) => {
    if (amount >= 1000000) {
      return `$${(amount / 1000000).toFixed(1)}M`;
    } else if (amount >= 1000) {
      return `$${(amount / 1000).toFixed(0)}K`;
    }
    return `$${amount.toLocaleString()}`;
  };

  const formatPercentage = (value: number) => `${(value * 100).toFixed(1)}%`;

  const getRankingColor = (ranking: string) => {
    switch (ranking) {
      case 'top_10': return 'bg-green-100 text-green-800';
      case 'top_25': return 'bg-blue-100 text-blue-800';
      case 'median': return 'bg-yellow-100 text-yellow-800';
      case 'below_median': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getRankingLabel = (ranking: string) => {
    switch (ranking) {
      case 'top_10': return 'Top 10%';
      case 'top_25': return 'Top 25%';
      case 'median': return 'Median';
      case 'below_median': return 'Below Median';
      default: return ranking;
    }
  };

  const getPercentileColor = (percentile: number) => {
    if (percentile >= 90) return 'text-green-600';
    if (percentile >= 75) return 'text-blue-600';
    if (percentile >= 50) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="space-y-6">
      {/* Percentile Rankings Overview */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <Target className="h-5 w-5 mr-2" />
          Performance Percentiles
        </h3>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
          <div className="text-center p-4 bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg">
            <p className={`text-2xl font-bold ${getPercentileColor(data.percentile_rankings.revenue_growth)}`}>
              {data.percentile_rankings.revenue_growth}%
            </p>
            <p className="text-sm text-blue-600">Revenue Growth</p>
          </div>
          
          <div className="text-center p-4 bg-gradient-to-br from-green-50 to-green-100 rounded-lg">
            <p className={`text-2xl font-bold ${getPercentileColor(data.percentile_rankings.customer_growth)}`}>
              {data.percentile_rankings.customer_growth}%
            </p>
            <p className="text-sm text-green-600">Customer Growth</p>
          </div>
          
          <div className="text-center p-4 bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg">
            <p className={`text-2xl font-bold ${getPercentileColor(data.percentile_rankings.funding_efficiency)}`}>
              {data.percentile_rankings.funding_efficiency}%
            </p>
            <p className="text-sm text-purple-600">Funding Efficiency</p>
          </div>
          
          <div className="text-center p-4 bg-gradient-to-br from-orange-50 to-orange-100 rounded-lg">
            <p className={`text-2xl font-bold ${getPercentileColor(data.percentile_rankings.team_experience)}`}>
              {data.percentile_rankings.team_experience}%
            </p>
            <p className="text-sm text-orange-600">Team Experience</p>
          </div>
          
          <div className="text-center p-4 bg-gradient-to-br from-teal-50 to-teal-100 rounded-lg">
            <p className={`text-2xl font-bold ${getPercentileColor(data.percentile_rankings.market_position)}`}>
              {data.percentile_rankings.market_position}%
            </p>
            <p className="text-sm text-teal-600">Market Position</p>
          </div>
        </div>
      </div>

      {/* Growth Comparisons */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <BarChart className="h-5 w-5 mr-2" />
          Growth Comparisons vs Peers
        </h3>
        
        <div className="space-y-4">
          {data.growth_comparisons.map((comparison, index) => (
            <div key={index} className="border rounded-lg p-4">
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-medium text-gray-900 capitalize">
                  {comparison.metric.replace('_', ' ')}
                </h4>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRankingColor(comparison.ranking)}`}>
                  {getRankingLabel(comparison.ranking)}
                </span>
              </div>
              
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">{companyName}</span>
                  <span className="font-semibold text-gray-900">
                    {comparison.metric.includes('rate') || comparison.metric.includes('growth') 
                      ? formatPercentage(comparison.company_value) 
                      : formatCurrency(comparison.company_value)
                    }
                  </span>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Peer Median</span>
                  <span className="text-gray-700">
                    {comparison.metric.includes('rate') || comparison.metric.includes('growth')
                      ? formatPercentage(comparison.peer_median)
                      : formatCurrency(comparison.peer_median)
                    }
                  </span>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">75th Percentile</span>
                  <span className="text-gray-700">
                    {comparison.metric.includes('rate') || comparison.metric.includes('growth')
                      ? formatPercentage(comparison.peer_75th_percentile)
                      : formatCurrency(comparison.peer_75th_percentile)
                    }
                  </span>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">90th Percentile</span>
                  <span className="text-gray-700">
                    {comparison.metric.includes('rate') || comparison.metric.includes('growth')
                      ? formatPercentage(comparison.peer_90th_percentile)
                      : formatCurrency(comparison.peer_90th_percentile)
                    }
                  </span>
                </div>
                
                {/* Progress bar visualization */}
                <div className="mt-3 bg-gray-200 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full ${
                      comparison.ranking === 'top_10' ? 'bg-green-500' :
                      comparison.ranking === 'top_25' ? 'bg-blue-500' :
                      comparison.ranking === 'median' ? 'bg-yellow-500' :
                      'bg-red-500'
                    }`}
                    style={{ 
                      width: `${Math.min(100, (comparison.company_value / comparison.peer_90th_percentile) * 100)}%`
                    }}
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Industry Averages */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <TrendingUp className="h-5 w-5 mr-2" />
          Industry Benchmarks
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <p className="text-xl font-bold text-gray-900">
              {formatPercentage(data.industry_averages.median_arr_growth)}
            </p>
            <p className="text-sm text-gray-600">Median ARR Growth</p>
          </div>
          
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <p className="text-xl font-bold text-gray-900">
              {formatPercentage(data.industry_averages.median_churn_rate)}
            </p>
            <p className="text-sm text-gray-600">Median Churn Rate</p>
          </div>
          
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <p className="text-xl font-bold text-gray-900">
              {data.industry_averages.median_cac_payback} months
            </p>
            <p className="text-sm text-gray-600">Median CAC Payback</p>
          </div>
          
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <p className="text-xl font-bold text-gray-900">
              {formatPercentage(data.industry_averages.median_gross_margin)}
            </p>
            <p className="text-sm text-gray-600">Median Gross Margin</p>
          </div>
        </div>
      </div>

      {/* Peer Companies */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <Users className="h-5 w-5 mr-2" />
          Peer Companies ({data.peer_group.length})
        </h3>
        
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Company
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Stage
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Total Funding
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  ARR
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Growth Rate
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {data.peer_group.slice(0, 10).map((peer, index) => (
                <tr key={index} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className="text-sm font-medium text-gray-900">{peer.name}</div>
                      <div className="text-sm text-gray-500">{peer.industry}</div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {peer.stage}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {formatCurrency(peer.total_funding)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {peer.metrics.revenue_arr ? formatCurrency(peer.metrics.revenue_arr) : 'N/A'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {peer.metrics.monthly_growth_rate ? formatPercentage(peer.metrics.monthly_growth_rate) : 'N/A'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          
          {data.peer_group.length > 10 && (
            <div className="mt-4 text-center text-gray-500 text-sm">
              +{data.peer_group.length - 10} more companies in peer group
            </div>
          )}
        </div>
      </div>
    </div>
  );
}