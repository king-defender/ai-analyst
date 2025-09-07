"""
Unit tests for file service functionality.
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
import tempfile
import os
from pathlib import Path
from fastapi import UploadFile
from io import BytesIO
from app.services.file_service import FileService


class TestFileService:
    """Test cases for FileService."""
    
    @pytest.fixture
    def file_service(self):
        """Create FileService instance."""
        service = FileService()
        # Use temporary directory for testing
        service.upload_dir = Path(tempfile.mkdtemp())
        return service
    
    @pytest.fixture
    def mock_upload_file(self, test_pdf_file):
        """Create mock UploadFile."""
        upload_file = Mock(spec=UploadFile)
        upload_file.filename = "test.pdf"
        upload_file.content_type = "application/pdf"
        upload_file.read = AsyncMock(return_value=test_pdf_file)
        return upload_file
    
    @pytest.mark.asyncio
    async def test_save_file_success(self, file_service, mock_upload_file):
        """Test successful file saving."""
        file_id = "test-file-123"
        
        file_path = await file_service.save_file(mock_upload_file, file_id)
        
        assert file_path is not None
        assert file_id in file_service.file_metadata
        
        metadata = file_service.file_metadata[file_id]
        assert metadata["filename"] == "test.pdf"
        assert metadata["content_type"] == "application/pdf"
        assert metadata["size"] > 0
    
    @pytest.mark.asyncio
    async def test_get_file_info_success(self, file_service, mock_upload_file):
        """Test retrieving file metadata."""
        file_id = "test-file-123"
        
        # Save file first
        await file_service.save_file(mock_upload_file, file_id)
        
        # Get file info
        file_info = await file_service.get_file_info(file_id)
        
        assert file_info is not None
        assert file_info["filename"] == "test.pdf"
        assert file_info["content_type"] == "application/pdf"
    
    @pytest.mark.asyncio
    async def test_get_file_info_not_found(self, file_service):
        """Test retrieving metadata for non-existent file."""
        file_info = await file_service.get_file_info("nonexistent-file")
        
        assert file_info is None
    
    @pytest.mark.asyncio
    async def test_delete_file_success(self, file_service, mock_upload_file):
        """Test successful file deletion."""
        file_id = "test-file-123"
        
        # Save file first
        await file_service.save_file(mock_upload_file, file_id)
        
        # Verify file exists
        assert file_id in file_service.file_metadata
        
        # Delete file
        result = await file_service.delete_file(file_id)
        
        assert result is True
        assert file_id not in file_service.file_metadata
    
    @pytest.mark.asyncio
    async def test_delete_file_not_found(self, file_service):
        """Test deleting non-existent file."""
        result = await file_service.delete_file("nonexistent-file")
        
        assert result is False
    
    @pytest.mark.asyncio
    async def test_get_extracted_content_pdf(self, file_service, mock_upload_file):
        """Test getting extracted content for PDF file."""
        file_id = "test-file-123"
        
        # Save file first
        await file_service.save_file(mock_upload_file, file_id)
        
        # Get extracted content
        content = await file_service.get_extracted_content(file_id)
        
        assert content is not None
        assert "PDF content extraction pending" in content
        assert "test.pdf" in content
    
    @pytest.mark.asyncio
    async def test_get_extracted_content_not_found(self, file_service):
        """Test getting extracted content for non-existent file."""
        content = await file_service.get_extracted_content("nonexistent-file")
        
        assert content is None
    
    @pytest.mark.asyncio
    async def test_save_file_handles_exception(self, file_service):
        """Test file service handles save exceptions gracefully."""
        # Create a mock file that will cause an error
        bad_upload_file = Mock(spec=UploadFile)
        bad_upload_file.filename = "test.pdf"
        bad_upload_file.content_type = "application/pdf"
        bad_upload_file.read = AsyncMock(side_effect=Exception("Read error"))
        
        with pytest.raises(Exception) as exc_info:
            await file_service.save_file(bad_upload_file, "test-file-123")
        
        assert "Failed to save file" in str(exc_info.value)
    
    def test_file_service_initialization(self, file_service):
        """Test FileService initializes correctly."""
        assert file_service.upload_dir.exists()
        assert isinstance(file_service.file_metadata, dict)
        assert len(file_service.file_metadata) == 0
    
    @pytest.mark.asyncio
    async def test_file_metadata_storage(self, file_service, mock_upload_file):
        """Test file metadata is stored correctly."""
        file_id = "test-file-123"
        
        await file_service.save_file(mock_upload_file, file_id)
        
        metadata = file_service.file_metadata[file_id]
        required_fields = ["filename", "file_path", "content_type", "size", "created_at"]
        
        for field in required_fields:
            assert field in metadata
            assert metadata[field] is not None