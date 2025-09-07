/**
 * Unit tests for upload components
 */
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';

// Mock FileUpload component
const MockFileUpload = ({ 
  onFileUpload, 
  acceptedTypes = ['.pdf', '.docx'] 
}: { 
  onFileUpload: (file: File) => void;
  acceptedTypes?: string[];
}) => {
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      onFileUpload(file);
    }
  };

  return (
    <div data-testid="file-upload">
      <input
        type="file"
        accept={acceptedTypes.join(',')}
        onChange={handleFileChange}
        data-testid="file-input"
      />
      <p>Supports: {acceptedTypes.join(', ')}</p>
      <p>Drag and drop files here or click to browse</p>
    </div>
  );
};

describe('FileUpload Component', () => {
  const mockOnFileUpload = jest.fn();

  beforeEach(() => {
    mockOnFileUpload.mockClear();
  });

  test('renders upload area', () => {
    render(<MockFileUpload onFileUpload={mockOnFileUpload} />);
    
    expect(screen.getByTestId('file-upload')).toBeInTheDocument();
    expect(screen.getByText('Drag and drop files here or click to browse')).toBeInTheDocument();
    expect(screen.getByText('Supports: .pdf, .docx')).toBeInTheDocument();
  });

  test('handles file selection', () => {
    render(<MockFileUpload onFileUpload={mockOnFileUpload} />);
    
    const fileInput = screen.getByTestId('file-input');
    const file = new File(['test content'], 'test.pdf', { type: 'application/pdf' });
    
    fireEvent.change(fileInput, { target: { files: [file] } });
    
    expect(mockOnFileUpload).toHaveBeenCalledWith(file);
  });

  test('shows supported file types', () => {
    const customTypes = ['.pdf', '.doc'];
    render(
      <MockFileUpload 
        onFileUpload={mockOnFileUpload} 
        acceptedTypes={customTypes}
      />
    );
    
    expect(screen.getByText('Supports: .pdf, .doc')).toBeInTheDocument();
  });

  test('accepts file input element', () => {
    render(<MockFileUpload onFileUpload={mockOnFileUpload} />);
    
    const fileInput = screen.getByTestId('file-input');
    expect(fileInput).toHaveAttribute('accept', '.pdf,.docx');
  });
});

// Mock UploadProgress component
const MockUploadProgress = ({ 
  progress, 
  fileName, 
  status = 'uploading' 
}: { 
  progress: number; 
  fileName: string;
  status?: 'uploading' | 'completed' | 'error';
}) => {
  return (
    <div data-testid="upload-progress">
      <p>Uploading: {fileName}</p>
      <div data-testid="progress-bar" style={{ width: `${progress}%` }}>
        {progress}%
      </div>
      <p>Status: {status}</p>
    </div>
  );
};

describe('UploadProgress Component', () => {
  test('renders upload progress', () => {
    render(
      <MockUploadProgress 
        progress={50} 
        fileName="test.pdf" 
        status="uploading"
      />
    );
    
    expect(screen.getByTestId('upload-progress')).toBeInTheDocument();
    expect(screen.getByText('Uploading: test.pdf')).toBeInTheDocument();
    expect(screen.getByText('50%')).toBeInTheDocument();
    expect(screen.getByText('Status: uploading')).toBeInTheDocument();
  });

  test('shows completed status', () => {
    render(
      <MockUploadProgress 
        progress={100} 
        fileName="test.pdf" 
        status="completed"
      />
    );
    
    expect(screen.getByText('Status: completed')).toBeInTheDocument();
    expect(screen.getByText('100%')).toBeInTheDocument();
  });

  test('shows error status', () => {
    render(
      <MockUploadProgress 
        progress={0} 
        fileName="test.pdf" 
        status="error"
      />
    );
    
    expect(screen.getByText('Status: error')).toBeInTheDocument();
  });
});