/**
 * Validation utilities for file uploads and data processing
 */

export interface FileValidationResult {
  isValid: boolean;
  error?: string;
}

/**
 * Validates if a file is a valid JSON file
 */
export async function validateJsonFile(file: File): Promise<FileValidationResult> {
  try {
    const text = await file.text();
    JSON.parse(text);
    return { isValid: true };
  } catch (error) {
    return {
      isValid: false,
      error: 'Invalid JSON file. Please ensure the file contains valid JSON data.'
    };
  }
}

/**
 * Validates file size
 */
export function validateFileSize(file: File, maxSizeBytes: number): FileValidationResult {
  if (file.size > maxSizeBytes) {
    const maxSizeMB = maxSizeBytes / 1024 / 1024;
    return {
      isValid: false,
      error: `File size must be less than ${maxSizeMB}MB`
    };
  }
  return { isValid: true };
}

/**
 * Validates file type based on extension
 */
export function validateFileType(file: File, acceptedTypes: string[]): FileValidationResult {
  const fileExtension = '.' + (file.name.split('.').pop()?.toLowerCase() || '');
  
  if (!acceptedTypes.includes(fileExtension)) {
    return {
      isValid: false,
      error: `File type not supported. Please upload: ${acceptedTypes.join(', ')}`
    };
  }
  
  return { isValid: true };
}

/**
 * Comprehensive file validation
 */
export async function validateFile(
  file: File, 
  acceptedTypes: string[], 
  maxSizeBytes: number
): Promise<FileValidationResult> {
  // Check file size
  const sizeValidation = validateFileSize(file, maxSizeBytes);
  if (!sizeValidation.isValid) {
    return sizeValidation;
  }

  // Check file type
  const typeValidation = validateFileType(file, acceptedTypes);
  if (!typeValidation.isValid) {
    return typeValidation;
  }

  // Additional JSON validation
  const fileExtension = '.' + (file.name.split('.').pop()?.toLowerCase() || '');
  if (fileExtension === '.json') {
    return await validateJsonFile(file);
  }

  return { isValid: true };
}