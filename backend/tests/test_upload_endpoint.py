"""
Test cases for the PDF upload endpoint functionality.
Uses direct HTTP requests to avoid TestClient compatibility issues.
"""
import requests
import tempfile
import os
import time
from typing import Dict, Any
import pytest


class TestUploadEndpoint:
    """Test upload endpoint without using FastAPI TestClient."""
    
    BASE_URL = "http://localhost:8000"
    UPLOAD_URL = f"{BASE_URL}/api/documents/upload"
    HEALTH_URL = f"{BASE_URL}/api/health"
    
    @classmethod
    def setup_class(cls):
        """Wait for server to be ready."""
        max_retries = 10
        for i in range(max_retries):
            try:
                response = requests.get(cls.HEALTH_URL, timeout=2)
                if response.status_code == 200:
                    break
            except:
                if i < max_retries - 1:
                    time.sleep(1)
                else:
                    raise Exception("Server not ready for testing")
    
    def test_server_is_running(self):
        """Test that server is running and healthy."""
        response = requests.get(self.HEALTH_URL)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_cors_preflight_request(self):
        """Test CORS preflight request handling."""
        headers = {
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type"
        }
        response = requests.options(self.UPLOAD_URL, headers=headers)
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
        assert "access-control-allow-methods" in response.headers
    
    def test_upload_no_file(self):
        """Test upload endpoint with no file."""
        headers = {"Origin": "http://localhost:3000"}
        response = requests.post(self.UPLOAD_URL, headers=headers)
        assert response.status_code == 422  # FastAPI validation error
        data = response.json()
        assert "detail" in data
        # Check CORS headers
        assert "access-control-allow-origin" in response.headers
    
    def test_upload_valid_pdf(self):
        """Test successful PDF upload."""
        # Create a test PDF file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(b"Test PDF content")
            tmp_file_path = tmp_file.name
        
        try:
            with open(tmp_file_path, "rb") as file:
                files = {"file": ("test.pdf", file, "application/pdf")}
                headers = {"Origin": "http://localhost:3000"}
                response = requests.post(self.UPLOAD_URL, files=files, headers=headers)
            
            assert response.status_code == 200
            data = response.json()
            assert "job_id" in data
            assert "file_id" in data
            assert data["filename"] == "test.pdf"
            assert data["status"] == "uploaded"
            
            # Check CORS headers
            assert "access-control-allow-origin" in response.headers
            
        finally:
            os.unlink(tmp_file_path)
    
    def test_upload_valid_txt(self):
        """Test successful TXT upload."""
        # Create a test TXT file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
            tmp_file.write(b"Test TXT content for startup analysis")
            tmp_file_path = tmp_file.name
        
        try:
            with open(tmp_file_path, "rb") as file:
                files = {"file": ("test.txt", file, "text/plain")}
                headers = {"Origin": "http://localhost:3000"}
                response = requests.post(self.UPLOAD_URL, files=files, headers=headers)
            
            assert response.status_code == 200
            data = response.json()
            assert "job_id" in data
            assert "file_id" in data
            assert data["filename"] == "test.txt"
            assert data["status"] == "uploaded"
            
        finally:
            os.unlink(tmp_file_path)
    
    def test_upload_invalid_file_type(self):
        """Test upload with invalid file type."""
        # Create a test image file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            tmp_file.write(b"Test image content")
            tmp_file_path = tmp_file.name
        
        try:
            with open(tmp_file_path, "rb") as file:
                files = {"file": ("test.jpg", file, "image/jpeg")}
                headers = {"Origin": "http://localhost:3000"}
                response = requests.post(self.UPLOAD_URL, files=files, headers=headers)
            
            assert response.status_code == 400
            data = response.json()
            assert "detail" in data
            assert "not supported" in data["detail"]
            assert "PDF, TXT, or DOCX" in data["detail"]
            
        finally:
            os.unlink(tmp_file_path)
    
    def test_upload_empty_file(self):
        """Test upload with empty file."""
        # Create an empty test file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file_path = tmp_file.name
        
        try:
            with open(tmp_file_path, "rb") as file:
                files = {"file": ("empty.pdf", file, "application/pdf")}
                headers = {"Origin": "http://localhost:3000"}
                response = requests.post(self.UPLOAD_URL, files=files, headers=headers)
            
            assert response.status_code == 400
            data = response.json()
            assert "detail" in data
            assert "empty" in data["detail"].lower()
            
        finally:
            os.unlink(tmp_file_path)
    
    def test_upload_file_too_large(self):
        """Test upload with file exceeding size limit."""
        # Create a large test file (larger than 50MB) using chunked writes to avoid high memory usage
        total_size = 51 * 1024 * 1024  # 51MB
        chunk_size = 1024 * 1024       # 1MB
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            written = 0
            chunk = b"x" * chunk_size
            while written < total_size:
                write_size = min(chunk_size, total_size - written)
                tmp_file.write(chunk[:write_size])
                written += write_size
            tmp_file_path = tmp_file.name
        
        try:
            with open(tmp_file_path, "rb") as file:
                files = {"file": ("large.pdf", file, "application/pdf")}
                headers = {"Origin": "http://localhost:3000"}
                response = requests.post(self.UPLOAD_URL, files=files, headers=headers)
            
            assert response.status_code == 413  # Payload Too Large
            data = response.json()
            assert "detail" in data
            assert "exceeds" in data["detail"]
            assert "50MB" in data["detail"]
            
        finally:
            os.unlink(tmp_file_path)
    
    def test_cors_headers_in_responses(self):
        """Test that all responses include proper CORS headers."""
        # Test with successful upload
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(b"Test content")
            tmp_file_path = tmp_file.name
        
        try:
            with open(tmp_file_path, "rb") as file:
                files = {"file": ("test.pdf", file, "application/pdf")}
                headers = {"Origin": "http://localhost:3000"}
                response = requests.post(self.UPLOAD_URL, files=files, headers=headers)
            
            # Check required CORS headers are present
            assert "access-control-allow-origin" in response.headers
            assert "access-control-allow-credentials" in response.headers
            assert "access-control-expose-headers" in response.headers
            
            # Check that credentials are allowed
            assert response.headers["access-control-allow-credentials"] == "true"
            
        finally:
            os.unlink(tmp_file_path)
    
    def test_file_extension_content_type_mismatch(self):
        """Test file with mismatched extension and content type."""
        # Create a test file with .pdf extension but text content type
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(b"Test content")
            tmp_file_path = tmp_file.name
        
        try:
            with open(tmp_file_path, "rb") as file:
                # Send with mismatched content type
                files = {"file": ("test.pdf", file, "text/plain")}
                headers = {"Origin": "http://localhost:3000"}
                response = requests.post(self.UPLOAD_URL, files=files, headers=headers)
            
            assert response.status_code == 400
            data = response.json()
            assert "detail" in data
            assert "does not match content type" in data["detail"]
            
        finally:
            os.unlink(tmp_file_path)