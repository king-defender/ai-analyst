"""
Unit tests for OCR service functionality.
"""
import pytest
from unittest.mock import Mock, patch
from app.services.ocr_service import OCRService


class TestOCRService:
    """Test cases for OCRService."""
    
    @pytest.fixture
    def ocr_service(self, mock_vision):
        """Create OCRService instance with mocked Vision API."""
        return OCRService()
    
    @pytest.mark.asyncio
    async def test_extract_text_from_image_success(self, ocr_service, mock_vision):
        """Test successful text extraction from image."""
        image_content = b"fake_image_content"
        
        result = await ocr_service.extract_text_from_image(image_content)
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert "Sample extracted text" in result
    
    @pytest.mark.asyncio
    async def test_extract_text_from_pdf_success(self, ocr_service, test_pdf_file):
        """Test successful text extraction from PDF."""
        with patch('app.services.ocr_service.pdf2image.convert_from_bytes') as mock_convert:
            # Mock PDF to image conversion
            mock_image = Mock()
            mock_image.save = Mock()
            mock_convert.return_value = [mock_image]
            
            result = await ocr_service.extract_text_from_pdf(test_pdf_file)
            
            assert isinstance(result, str)
            assert len(result) >= 0  # Can be empty if no text detected
    
    @pytest.mark.asyncio
    async def test_process_document_pdf(self, ocr_service, test_pdf_file):
        """Test document processing for PDF file."""
        result = await ocr_service.process_document(test_pdf_file, "application/pdf")
        
        assert "extracted_text" in result
        assert "confidence_score" in result
        assert "processing_time" in result
        assert isinstance(result["extracted_text"], str)
        assert isinstance(result["confidence_score"], (int, float))
    
    @pytest.mark.asyncio
    async def test_process_document_image(self, ocr_service):
        """Test document processing for image file."""
        image_content = b"fake_image_content"
        
        result = await ocr_service.process_document(image_content, "image/jpeg")
        
        assert "extracted_text" in result
        assert "confidence_score" in result
        assert "processing_time" in result
    
    @pytest.mark.asyncio
    async def test_process_document_unsupported_type(self, ocr_service):
        """Test document processing for unsupported file type."""
        content = b"fake_content"
        
        with pytest.raises(ValueError):
            await ocr_service.process_document(content, "text/plain")
    
    def test_clean_extracted_text(self, ocr_service):
        """Test text cleaning functionality."""
        dirty_text = "  This is   a test\n\nwith  extra   spaces  \n  "
        expected = "This is a test\n\nwith extra spaces"
        
        result = ocr_service.clean_extracted_text(dirty_text)
        
        assert result == expected
    
    def test_calculate_confidence_score(self, ocr_service):
        """Test confidence score calculation."""
        # Mock Vision API response with confidence scores
        mock_response = Mock()
        mock_annotation = Mock()
        mock_annotation.confidence = 0.95
        mock_response.text_annotations = [mock_annotation]
        
        result = ocr_service.calculate_confidence_score(mock_response)
        
        assert isinstance(result, float)
        assert 0 <= result <= 1
    
    @pytest.mark.asyncio
    async def test_extract_text_handles_error(self, ocr_service):
        """Test OCR service handles Vision API errors gracefully."""
        with patch.object(ocr_service.client, 'text_detection') as mock_detect:
            mock_response = Mock()
            mock_response.error.message = "API Error"
            mock_detect.return_value = mock_response
            
            result = await ocr_service.extract_text_from_image(b"fake_content")
            
            assert result == ""  # Should return empty string on error