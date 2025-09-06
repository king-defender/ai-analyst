#!/usr/bin/env python3
"""
Quick test script to validate new file type support
"""
import asyncio
import json
import io
import tempfile
import os
from pathlib import Path

# Add the backend directory to Python path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from fastapi.testclient import TestClient
from main import app

def create_test_files():
    """Create sample test files for each supported format"""
    test_files = {}
    
    # JSON file
    json_data = {
        "company": "Test Company",
        "revenue": 1000000,
        "employees": 50
    }
    json_content = json.dumps(json_data, indent=2).encode('utf-8')
    test_files['test.json'] = ('application/json', json_content)
    
    # Simple DOC content (minimal binary format)
    doc_content = b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1\x00\x00\x00\x00' + b'Test DOC content' * 10
    test_files['test.doc'] = ('application/msword', doc_content)
    
    # Simple XLS content (minimal binary format)
    xls_content = b'\x09\x08\x08\x00\x00\x00\x10\x00' + b'Test XLS content' * 10
    test_files['test.xls'] = ('application/vnd.ms-excel', xls_content)
    
    # Simple XLSX content (ZIP format)
    xlsx_content = b'PK\x03\x04\x14\x00\x00\x00\x08\x00' + b'Test XLSX content' * 10
    test_files['test.xlsx'] = ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', xlsx_content)
    
    return test_files

def test_file_upload(filename, content_type, content):
    """Test file upload for a specific file type"""
    try:
        client = TestClient(app)
        
        files = {"file": (filename, io.BytesIO(content), content_type)}
        response = client.post("/api/documents/upload", files=files)
        
        print(f"Testing {filename} ({content_type}):")
        print(f"  Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Success: {data.get('filename', 'unknown')}")
            print(f"  Job ID: {data.get('job_id', 'N/A')}")
            print(f"  File ID: {data.get('file_id', 'N/A')}")
        else:
            print(f"  ❌ Error: {response.text}")
        
        client.close()
        print()
        
    except Exception as e:
        print(f"  ❌ Exception: {str(e)}")
        print()

def main():
    print("Testing new file type support in AI Analyst backend\n")
    print("=" * 60)
    
    test_files = create_test_files()
    
    for filename, (content_type, content) in test_files.items():
        test_file_upload(filename, content_type, content)
    
    print("=" * 60)
    print("Test completed!")

if __name__ == "__main__":
    main()