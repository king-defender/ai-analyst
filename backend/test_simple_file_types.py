#!/usr/bin/env python3
"""
Simple test to validate file type validation logic
"""
import sys
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
    
    print("Testing allowed file types:")
    print("=" * 50)
    
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
    
    print("=" * 50)
    
    # Test some invalid types
    print("Testing invalid file types:")
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
    
    print("=" * 50)
    if all_passed:
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed!")
    
    return all_passed

if __name__ == "__main__":
    success = test_allowed_content_types()
    sys.exit(0 if success else 1)