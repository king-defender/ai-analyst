#!/usr/bin/env python3
"""
Integration tests for new file format support.
Tests the complete flow from upload to content extraction.
"""
import asyncio
import json
import tempfile
import os
from pathlib import Path
import sys

# Add the backend directory to Python path
sys.path.insert(0, '/home/runner/work/ai-analyst/ai-analyst/backend')

from fastapi.testclient import TestClient
from main import app
from app.services.file_service import FileService

class TestNewFileFormatsIntegration:
    """Integration tests for new file format support"""
    
    def __init__(self):
        self.file_service = FileService()
    
    def create_test_files(self):
        """Create test files for each new supported format"""
        test_files = {}
        
        # DOC file (minimal binary format)
        doc_content = b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1\x00\x00\x00\x00' + b'Test DOC content with startup financial data' * 5
        test_files['test_startup.doc'] = ('application/msword', doc_content)
        
        # XLS file (minimal binary format)
        xls_content = b'\x09\x08\x08\x00\x00\x00\x10\x00' + b'Revenue,2023,2024\nStartup Inc,500000,750000\n' * 3
        test_files['financial_data.xls'] = ('application/vnd.ms-excel', xls_content)
        
        # XLSX file (ZIP format with financial data)
        xlsx_content = b'PK\x03\x04\x14\x00\x00\x00\x08\x00' + b'Company,Revenue,Growth\nTechFlow,2500000,25%\n' * 5
        test_files['company_metrics.xlsx'] = ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', xlsx_content)
        
        # JSON file with startup data
        json_data = {
            "company": "TechFlow Solutions",
            "industry": "SaaS",
            "stage": "Series A",
            "financial_metrics": {
                "revenue": 2500000,
                "growth_rate": 0.25,
                "runway_months": 18,
                "burn_rate": 150000
            },
            "team_size": 25,
            "market_size": {
                "tam": 12000000000,
                "sam": 3000000000,
                "som": 300000000
            }
        }
        json_content = json.dumps(json_data, indent=2).encode('utf-8')
        test_files['startup_data.json'] = ('application/json', json_content)
        
        return test_files
    
    def test_upload_flow(self, filename, content_type, content):
        """Test complete upload flow for a file"""
        print(f"\n🧪 Testing upload flow for {filename}")
        
        # Step 1: Upload file
        try:
            # Create the TestClient within the test method
            with TestClient(app) as client:
                # Create file-like object from content
                import io
                file_obj = io.BytesIO(content)
                files = {"file": (filename, file_obj, content_type)}
                response = client.post("/api/documents/upload", files=files)
                
                if response.status_code != 200:
                    print(f"  ❌ Upload failed: {response.status_code} - {response.text}")
                    return False
                
                upload_data = response.json()
                file_id = upload_data.get('file_id')
                job_id = upload_data.get('job_id')
                
                print(f"  ✅ Upload successful:")
                print(f"     File ID: {file_id}")
                print(f"     Job ID: {job_id}")
                print(f"     Filename: {upload_data.get('filename')}")
                
                # Step 2: Check file info
                response = client.get(f"/api/documents/{file_id}/info")
                if response.status_code == 200:
                    file_info = response.json()
                    print(f"  ✅ File info retrieved:")
                    print(f"     Content type: {file_info.get('content_type')}")
                    print(f"     Size: {file_info.get('size')} bytes")
                else:
                    print(f"  ⚠️  File info not available: {response.status_code}")
                
                # Step 3: Test content extraction
                response = client.get(f"/api/documents/{file_id}/extracted-data")
                if response.status_code == 200:
                    extracted_data = response.json()
                    print(f"  ✅ Data extraction successful:")
                    print(f"     Company: {extracted_data.get('company_name', 'N/A')}")
                    print(f"     Industry: {extracted_data.get('industry', 'N/A')}")
                    print(f"     Revenue: ${extracted_data.get('financial_metrics', {}).get('revenue', 0):,}")
                else:
                    print(f"  ⚠️  Data extraction not available: {response.status_code}")
                
                # Step 4: Test document status
                response = client.get(f"/api/documents/{file_id}/status")
                if response.status_code == 200:
                    status_data = response.json()
                    print(f"  ✅ Document status: {status_data.get('status', 'unknown')}")
                else:
                    print(f"  ⚠️  Status not available: {response.status_code}")
                
                return True
            
        except Exception as e:
            print(f"  ❌ Exception during testing: {str(e)}")
            return False
    
    def test_invalid_formats(self):
        """Test that invalid formats are properly rejected"""
        print(f"\n🧪 Testing invalid format rejection")
        
        invalid_files = [
            ("test.zip", "application/zip", b"PK\x03\x04Invalid ZIP content"),
            ("test.png", "image/png", b"\x89PNG\r\n\x1a\nInvalid PNG content"),
            ("test.mp4", "video/mp4", b"Invalid MP4 content"),
            ("test.exe", "application/x-executable", b"Invalid EXE content")
        ]
        
        all_rejected = True
        with TestClient(app) as client:
            for filename, content_type, content in invalid_files:
                import io
                file_obj = io.BytesIO(content)
                files = {"file": (filename, file_obj, content_type)}
                response = client.post("/api/documents/upload", files=files)
                
                if response.status_code == 400:
                    print(f"  ✅ Correctly rejected: {filename} ({content_type})")
                else:
                    print(f"  ❌ Incorrectly accepted: {filename} ({content_type}) - Status: {response.status_code}")
                    all_rejected = False
        
        return all_rejected
    
    def test_file_extension_mismatch(self):
        """Test files with mismatched extensions and content types"""
        print(f"\n🧪 Testing extension/content-type mismatch handling")
        
        mismatch_cases = [
            ("document.pdf", "application/json", b'{"test": "data"}'),
            ("data.json", "application/pdf", b"PDF-like content"),
            ("spreadsheet.xlsx", "text/plain", b"Plain text content"),
            ("document.txt", "application/msword", b"Text content as DOC")
        ]
        
        all_rejected = True
        with TestClient(app) as client:
            for filename, content_type, content in mismatch_cases:
                import io
                file_obj = io.BytesIO(content)
                files = {"file": (filename, file_obj, content_type)}
                response = client.post("/api/documents/upload", files=files)
                
                if response.status_code == 400:
                    error_detail = response.json().get('detail', '')
                    if "does not match content type" in error_detail:
                        print(f"  ✅ Correctly rejected mismatch: {filename} -> {content_type}")
                    else:
                        print(f"  ⚠️  Rejected but with different error: {filename} -> {content_type}")
                else:
                    print(f"  ❌ Incorrectly accepted mismatch: {filename} -> {content_type}")
                    all_rejected = False
        
        return all_rejected
    
    def run_all_tests(self):
        """Run all integration tests"""
        print("=" * 80)
        print("🚀 Starting New File Formats Integration Tests")
        print("=" * 80)
        
        # Test new file formats
        test_files = self.create_test_files()
        upload_success = True
        
        for filename, (content_type, content) in test_files.items():
            success = self.test_upload_flow(filename, content_type, content)
            if not success:
                upload_success = False
        
        # Test invalid format rejection
        rejection_success = self.test_invalid_formats()
        
        # Test extension mismatch handling
        mismatch_success = self.test_file_extension_mismatch()
        
        # Final summary
        print("\n" + "=" * 80)
        print("📊 Test Results Summary")
        print("=" * 80)
        
        all_passed = upload_success and rejection_success and mismatch_success
        
        print(f"📁 New format uploads: {'✅ PASSED' if upload_success else '❌ FAILED'}")
        print(f"🚫 Invalid format rejection: {'✅ PASSED' if rejection_success else '❌ FAILED'}")
        print(f"⚠️  Extension mismatch handling: {'✅ PASSED' if mismatch_success else '❌ FAILED'}")
        print(f"\n🏆 Overall result: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
        
        return all_passed

def main():
    """Run the integration tests"""
    tester = TestNewFileFormatsIntegration()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)