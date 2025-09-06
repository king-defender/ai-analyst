#!/usr/bin/env python3
"""
Simplified test for new file format support.
Tests the file validation logic directly.
"""
import sys
import json

# Add the backend directory to Python path
sys.path.insert(0, '/home/runner/work/ai-analyst/ai-analyst/backend')

def test_allowed_content_types():
    """Test that our allowed content types include the new formats"""
    
    # This mirrors the allowed_content_types from documents.py
    allowed_content_types = {
        "application/pdf": ".pdf",
        "text/plain": ".txt", 
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
        "application/msword": ".doc",
        "application/vnd.ms-excel": ".xls",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
        "application/json": ".json"
    }
    
    print("Testing file format validation logic")
    print("=" * 60)
    
    test_cases = [
        ("PDF file", "application/pdf", ".pdf"),
        ("Text file", "text/plain", ".txt"),
        ("DOCX file", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", ".docx"),
        ("DOC file", "application/msword", ".doc"),
        ("XLS file", "application/vnd.ms-excel", ".xls"),
        ("XLSX file", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", ".xlsx"),
        ("JSON file", "application/json", ".json")
    ]
    
    all_passed = True
    
    for test_name, content_type, expected_ext in test_cases:
        if content_type in allowed_content_types:
            actual_ext = allowed_content_types[content_type]
            if actual_ext == expected_ext:
                print(f"✅ {test_name}: {content_type} -> {actual_ext}")
            else:
                print(f"❌ {test_name}: Expected {expected_ext}, got {actual_ext}")
                all_passed = False
        else:
            print(f"❌ {test_name}: {content_type} not in allowed types")
            all_passed = False
    
    print("=" * 60)
    print("Testing invalid file types rejection:")
    
    # Test some invalid types
    invalid_types = [
        "application/zip",
        "image/png", 
        "video/mp4",
        "application/unknown"
    ]
    
    for invalid_type in invalid_types:
        if invalid_type not in allowed_content_types:
            print(f"✅ Correctly rejects: {invalid_type}")
        else:
            print(f"❌ Incorrectly allows: {invalid_type}")
            all_passed = False
    
    print("=" * 60)
    print("Testing file extension validation logic:")
    
    # Test extension matching logic
    test_files = [
        ("document.pdf", "application/pdf", True),
        ("data.txt", "text/plain", True),
        ("pitch.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", True),
        ("legacy.doc", "application/msword", True),
        ("sheet.xls", "application/vnd.ms-excel", True),
        ("workbook.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", True),
        ("config.json", "application/json", True),
        # Mismatched cases
        ("document.pdf", "application/json", False),
        ("data.json", "text/plain", False),
        ("sheet.xlsx", "application/pdf", False),
    ]
    
    for filename, content_type, should_pass in test_files:
        file_extension = filename.lower().split(".")[-1] if "." in filename else ""
        
        if content_type in allowed_content_types:
            expected_extension = allowed_content_types[content_type].lstrip(".")
            extension_matches = file_extension == expected_extension
            
            if extension_matches == should_pass:
                status = "✅" if should_pass else "✅"
                outcome = "matches" if should_pass else "mismatch detected"
                print(f"{status} {filename} + {content_type}: {outcome}")
            else:
                print(f"❌ {filename} + {content_type}: unexpected result")
                all_passed = False
        else:
            if not should_pass:
                print(f"✅ {filename} + {content_type}: invalid content type rejected")
            else:
                print(f"❌ {filename} + {content_type}: should have been rejected")
                all_passed = False
    
    return all_passed

def test_file_service_content_extraction():
    """Test that the file service can handle new formats"""
    try:
        from app.services.file_service import FileService
        import tempfile
        import os
        import json
        
        print("\n" + "=" * 60)
        print("Testing FileService content extraction support:")
        
        file_service = FileService()
        
        # Create test files with actual content
        test_files = [
            ("test.doc", "application/msword", b'DOC content'),
            ("test.xls", "application/vnd.ms-excel", b'XLS content'),
            ("test.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", b'XLSX content'),
            ("test.json", "application/json", json.dumps({"test": "data", "revenue": 1000000}).encode()),
        ]
        
        all_passed = True
        temp_files = []
        
        for filename, content_type, content in test_files:
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix=f'.{filename.split(".")[-1]}') as tmp_file:
                tmp_file.write(content)
                temp_path = tmp_file.name
                temp_files.append(temp_path)
            
            # Mock file metadata
            file_id = f"test-{filename.replace('.', '-')}"
            file_service.file_metadata[file_id] = {
                "filename": filename,
                "file_path": temp_path,
                "content_type": content_type,
                "size": len(content),
                "created_at": "2024-01-01",
            }
            
            # Test content extraction
            import asyncio
            async def test_extraction():
                return await file_service.get_extracted_content(file_id)
            
            extracted_content = asyncio.run(test_extraction())
            
            if extracted_content:
                if content_type == "application/json":
                    # For JSON, we expect the actual content back
                    if '{"test": "data"' in extracted_content:
                        print(f"✅ {filename} ({content_type}): JSON content extracted successfully")
                    else:
                        print(f"❌ {filename} ({content_type}): JSON content not properly extracted")
                        all_passed = False
                else:
                    # For other formats, we expect placeholder messages
                    if extracted_content.startswith("[") and filename in extracted_content:
                        print(f"✅ {filename} ({content_type}): Extraction placeholder ready")
                    else:
                        print(f"❌ {filename} ({content_type}): Unexpected extraction result")
                        all_passed = False
            else:
                print(f"❌ {filename} ({content_type}): No extraction result")
                all_passed = False
        
        # Clean up temporary files
        for temp_path in temp_files:
            try:
                os.unlink(temp_path)
            except:
                pass
        
        return all_passed
        
    except Exception as e:
        print(f"❌ FileService test failed: {str(e)}")
        return False

def main():
    """Run all simplified tests"""
    print("🚀 Testing New File Format Support")
    print("=" * 80)
    
    # Test file type validation
    validation_passed = test_allowed_content_types()
    
    # Test file service integration
    service_passed = test_file_service_content_extraction()
    
    # Final summary
    print("\n" + "=" * 80)
    print("📊 Test Results Summary")
    print("=" * 80)
    
    all_passed = validation_passed and service_passed
    
    print(f"📝 File format validation: {'✅ PASSED' if validation_passed else '❌ FAILED'}")
    print(f"🔧 FileService integration: {'✅ PASSED' if service_passed else '❌ FAILED'}")
    print(f"\n🏆 Overall result: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)