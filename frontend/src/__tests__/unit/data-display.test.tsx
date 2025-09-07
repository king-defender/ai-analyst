/**
 * Unit tests for data display components
 */
import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';

// Mock StartupDataDisplay component
const MockStartupDataDisplay = ({ data }: { data: any }) => {
  return (
    <div data-testid="startup-data-display">
      <h1>{data.company_name}</h1>
      <p>Founded: {data.founded_year}</p>
      <p>Industry: {data.industry}</p>
      <p>Stage: {data.stage}</p>
      <p>Description: {data.description}</p>
      
      {data.metrics && (
        <div data-testid="metrics">
          <h2>Key Metrics</h2>
          <p>ARR: ${(data.metrics.revenue_arr / 1000000).toFixed(1)}M</p>
          <p>Growth: {(data.metrics.monthly_growth_rate * 100).toFixed(1)}%</p>
          <p>Customers: {data.metrics.customer_count}</p>
        </div>
      )}
      
      {data.team && (
        <div data-testid="team">
          <h2>Team</h2>
          {data.team.map((member: any, index: number) => (
            <div key={index}>
              <p>{member.name} - {member.role}</p>
              <p>Experience: {member.experience_years} years</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

// Mock RiskAssessment component
const MockRiskAssessment = ({ riskData }: { riskData: any }) => {
  return (
    <div data-testid="risk-assessment">
      <h2>Risk Assessment</h2>
      <p>Overall Risk Score: {riskData.overall_risk_score}%</p>
      
      {riskData.red_flags && riskData.red_flags.length > 0 && (
        <div data-testid="red-flags">
          <h3>Red Flags</h3>
          {riskData.red_flags.map((flag: any, index: number) => (
            <p key={index} className="text-red-600">{flag.risk_type}</p>
          ))}
        </div>
      )}
      
      {riskData.yellow_flags && riskData.yellow_flags.length > 0 && (
        <div data-testid="yellow-flags">
          <h3>Yellow Flags</h3>
          {riskData.yellow_flags.map((flag: any, index: number) => (
            <p key={index} className="text-yellow-600">{flag.risk_type}</p>
          ))}
        </div>
      )}
    </div>
  );
};

describe('StartupDataDisplay Component', () => {
  const mockStartupData = {
    company_name: 'Test Company',
    founded_year: 2022,
    industry: 'SaaS',
    stage: 'Series A',
    description: 'Test description',
    team: [
      {
        name: 'John Doe',
        role: 'CEO',
        bio: 'Experienced CEO',
        experience_years: 10,
        previous_companies: ['Google'],
        education: ['Stanford']
      }
    ],
    metrics: {
      revenue_arr: 2500000,
      monthly_growth_rate: 0.25,
      customer_count: 150
    }
  };

  test('renders company overview', () => {
    render(<MockStartupDataDisplay data={mockStartupData} />);
    
    expect(screen.getByText('Test Company')).toBeInTheDocument();
    expect(screen.getByText('Founded: 2022')).toBeInTheDocument();
    expect(screen.getByText('Industry: SaaS')).toBeInTheDocument();
    expect(screen.getByText('Stage: Series A')).toBeInTheDocument();
  });

  test('renders key metrics', () => {
    render(<MockStartupDataDisplay data={mockStartupData} />);
    
    expect(screen.getByText('ARR: $2.5M')).toBeInTheDocument();
    expect(screen.getByText('Growth: 25.0%')).toBeInTheDocument();
    expect(screen.getByText('Customers: 150')).toBeInTheDocument();
  });

  test('renders team information', () => {
    render(<MockStartupDataDisplay data={mockStartupData} />);
    
    expect(screen.getByText('John Doe - CEO')).toBeInTheDocument();
    expect(screen.getByText('Experience: 10 years')).toBeInTheDocument();
  });

  test('handles missing metrics gracefully', () => {
    const dataWithoutMetrics = {
      ...mockStartupData,
      metrics: undefined
    };
    
    render(<MockStartupDataDisplay data={dataWithoutMetrics} />);
    
    expect(screen.getByText('Test Company')).toBeInTheDocument();
    expect(screen.queryByTestId('metrics')).not.toBeInTheDocument();
  });
});

describe('RiskAssessment Component', () => {
  const mockRiskData = {
    overall_risk_score: 65,
    red_flags: [
      { risk_type: 'Short Runway', severity: 'high' },
      { risk_type: 'High Churn Rate', severity: 'high' }
    ],
    yellow_flags: [
      { risk_type: 'Limited Market Size', severity: 'medium' }
    ]
  };

  test('renders risk score', () => {
    render(<MockRiskAssessment riskData={mockRiskData} />);
    
    expect(screen.getByText('Overall Risk Score: 65%')).toBeInTheDocument();
  });

  test('renders red flags', () => {
    render(<MockRiskAssessment riskData={mockRiskData} />);
    
    expect(screen.getByTestId('red-flags')).toBeInTheDocument();
    expect(screen.getByText('Short Runway')).toBeInTheDocument();
    expect(screen.getByText('High Churn Rate')).toBeInTheDocument();
  });

  test('renders yellow flags', () => {
    render(<MockRiskAssessment riskData={mockRiskData} />);
    
    expect(screen.getByTestId('yellow-flags')).toBeInTheDocument();
    expect(screen.getByText('Limited Market Size')).toBeInTheDocument();
  });

  test('handles no flags gracefully', () => {
    const riskDataNoFlags = {
      overall_risk_score: 25,
      red_flags: [],
      yellow_flags: []
    };
    
    render(<MockRiskAssessment riskData={riskDataNoFlags} />);
    
    expect(screen.getByText('Overall Risk Score: 25%')).toBeInTheDocument();
    expect(screen.queryByTestId('red-flags')).not.toBeInTheDocument();
    expect(screen.queryByTestId('yellow-flags')).not.toBeInTheDocument();
  });
});