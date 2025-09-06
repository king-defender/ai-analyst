import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import FileUpload from '../components/upload/FileUpload';

describe('FileUpload Component', () => {
  const mockOnFileUpload = jest.fn();

  beforeEach(() => {
    mockOnFileUpload.mockClear();
  });

  test('renders upload interface', () => {
    render(<FileUpload onFileUpload={mockOnFileUpload} />);
    
    expect(screen.getByText('Upload your pitch deck')).toBeInTheDocument();
    expect(screen.getByText('Drag & drop or click to select')).toBeInTheDocument();
    expect(screen.getByText('Supports: .pdf, .txt, .docx')).toBeInTheDocument();
  });

  test('shows uploading state', () => {
    render(<FileUpload onFileUpload={mockOnFileUpload} isUploading={true} />);
    
    expect(screen.getByText('Uploading...')).toBeInTheDocument();
  });

  test('displays error with retry button for retryable errors', () => {
    const mockRetry = jest.fn();
    const mockApiError = {
      name: 'RateLimitError',
      type: 'rate_limit' as const,
      message: 'Too many requests. Please wait a moment before trying again.',
      status: 429,
      retryable: true,
      retryAfter: '60'
    };
    
    render(
      <FileUpload 
        onFileUpload={mockOnFileUpload} 
        uploadStatus="error"
        error={mockApiError}
        onRetry={mockRetry}
      />
    );
    
    expect(screen.getByText('Rate limit exceeded')).toBeInTheDocument();
    expect(screen.getByText('Too many requests. Please wait a moment before trying again.')).toBeInTheDocument();
    expect(screen.getByText('Try Again')).toBeInTheDocument();
  });

  test('displays error without retry button for non-retryable errors', () => {
    const mockApiError = {
      name: 'FileTooLargeError',
      type: 'file_too_large' as const,
      message: 'File size exceeds the maximum limit of 50MB.',
      status: 413,
      retryable: false
    };
    
    render(
      <FileUpload 
        onFileUpload={mockOnFileUpload} 
        uploadStatus="error"
        error={mockApiError}
      />
    );
    
    expect(screen.getByText('File too large')).toBeInTheDocument();
    expect(screen.getByText('File size exceeds the maximum limit of 50MB.')).toBeInTheDocument();
    expect(screen.queryByText('Try Again')).not.toBeInTheDocument();
  });

  test('displays custom accepted types', () => {
    const customTypes = ['.pdf', '.doc'];
    render(
      <FileUpload 
        onFileUpload={mockOnFileUpload} 
        acceptedTypes={customTypes}
      />
    );
    
    expect(screen.getByText('Supports: .pdf, .doc')).toBeInTheDocument();
  });
});

describe('JobTracker Component', () => {
  test('renders loading state', () => {
    const { JobTracker } = require('../components/status/JobTracker');
    
    render(<JobTracker jobId="test-job-123" />);
    
    expect(screen.getByText('Loading job status...')).toBeInTheDocument();
  });
});

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
    },
    financial_data: {
      total_funding_raised: 10000000,
      unit_economics: {
        cac: 500,
        ltv: 2000
      }
    },
    market_data: {
      total_addressable_market: 50000000000,
      serviceable_addressable_market: 8000000000,
      target_market_size: 500000000,
      market_growth_rate: 0.15,
      market_position: 'Leader'
    },
    product_info: {
      product_name: 'Test Product',
      product_type: 'SaaS',
      key_features: ['Feature 1', 'Feature 2'],
      development_stage: 'Production'
    },
    traction: {
      user_growth_metrics: {
        monthly_active_users: 5000
      },
      business_metrics: {
        revenue_growth: 0.25
      },
      partnerships: [],
      awards_recognition: []
    },
    funding_history: []
  };

  test('renders company overview', () => {
    const { default: StartupDataDisplay } = require('../components/data/StartupDataDisplay');
    
    render(<StartupDataDisplay data={mockStartupData} />);
    
    expect(screen.getByText('Test Company')).toBeInTheDocument();
    expect(screen.getByText('2022')).toBeInTheDocument();
    expect(screen.getByText('SaaS')).toBeInTheDocument();
    expect(screen.getByText('Series A')).toBeInTheDocument();
  });

  test('renders key metrics', () => {
    const { default: StartupDataDisplay } = require('../components/data/StartupDataDisplay');
    
    render(<StartupDataDisplay data={mockStartupData} />);
    
    expect(screen.getByText('$2.5M')).toBeInTheDocument(); // ARR
    expect(screen.getByText('25.0%')).toBeInTheDocument(); // Growth rate
    expect(screen.getByText('150')).toBeInTheDocument(); // Customers
  });

  test('renders team information', () => {
    const { default: StartupDataDisplay } = require('../components/data/StartupDataDisplay');
    
    render(<StartupDataDisplay data={mockStartupData} />);
    
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('CEO')).toBeInTheDocument();
    expect(screen.getByText('10 years')).toBeInTheDocument();
  });
});

describe('Utility Functions', () => {
  test('formatCurrency works correctly', () => {
    const { formatCurrency } = require('../utils/format');
    
    expect(formatCurrency(1000)).toBe('$1K');
    expect(formatCurrency(1000000)).toBe('$1.0M');
    expect(formatCurrency(1000000000)).toBe('$1.0B');
    expect(formatCurrency(500)).toBe('$500');
  });

  test('formatPercentage works correctly', () => {
    const { formatPercentage } = require('../utils/format');
    
    expect(formatPercentage(0.25)).toBe('25.0%');
    expect(formatPercentage(0.1)).toBe('10.0%');
    expect(formatPercentage(1.5)).toBe('150.0%');
  });

  test('getInitials works correctly', () => {
    const { getInitials } = require('../utils/format');
    
    expect(getInitials('John Doe')).toBe('JD');
    expect(getInitials('Sarah Michelle Chen')).toBe('SM');
    expect(getInitials('Single')).toBe('Si');
  });
});

describe('API Client', () => {
  test('API client can be imported', () => {
    const { apiClient } = require('../lib/api');
    expect(apiClient).toBeDefined();
  });
});

describe('Hooks', () => {
  test('useFileUpload hook can be imported', () => {
    const { useFileUpload } = require('../hooks/useFileUpload');
    expect(useFileUpload).toBeDefined();
  });

  test('useJobStatus hook can be imported', () => {
    const { useJobStatus } = require('../src/hooks/useJobStatus');
    expect(useJobStatus).toBeDefined();
  });
});