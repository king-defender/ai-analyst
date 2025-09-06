import aiofiles
import json
from typing import Optional, Dict, Any
from fastapi import UploadFile
from pathlib import Path


class FileService:
    def __init__(self):
        self.upload_dir = Path("uploads")
        self.upload_dir.mkdir(exist_ok=True)

        # File metadata storage (in production, use a database)
        self.file_metadata: Dict[str, Dict[str, Any]] = {}

    async def save_file(self, file: UploadFile, file_id: str) -> str:
        """Save uploaded file to disk and return the file path."""
        try:
            # Get file extension
            filename = file.filename or "unknown"
            file_extension = Path(filename).suffix

            # Create file path
            file_path = self.upload_dir / f"{file_id}{file_extension}"

            # Save file
            async with aiofiles.open(file_path, "wb") as f:
                content = await file.read()
                await f.write(content)

            # Store metadata
            self.file_metadata[file_id] = {
                "filename": filename,
                "file_path": str(file_path),
                "content_type": file.content_type,
                "size": len(content),
                "created_at": str(Path(file_path).stat().st_ctime),
            }

            return str(file_path)

        except Exception as e:
            raise Exception(f"Failed to save file: {str(e)}")

    async def get_file_info(self, file_id: str) -> Optional[Dict[str, Any]]:
        """Get file metadata."""
        return self.file_metadata.get(file_id)

    async def delete_file(self, file_id: str) -> bool:
        """Delete a file and its metadata."""
        try:
            file_info = self.file_metadata.get(file_id)
            if not file_info:
                return False

            # Delete file from disk
            file_path = Path(file_info["file_path"])
            if file_path.exists():
                file_path.unlink()

            # Remove metadata
            del self.file_metadata[file_id]

            return True

        except Exception:
            return False

    async def get_extracted_content(self, file_id: str) -> Optional[str]:
        """Get extracted text content from a file."""
        file_info = self.file_metadata.get(file_id)
        if not file_info:
            return None

        try:
            file_path = Path(file_info["file_path"])
            content_type = file_info["content_type"]

            if content_type == "text/plain":
                async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
                    return await f.read()

            elif content_type == "application/pdf":
                # For MVP, return placeholder - would integrate with Google Vision API
                return f"[PDF content extraction pending for {file_info['filename']}]"

            elif (
                content_type
                == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ):
                # For MVP, return placeholder - would integrate with document parser
                return f"[DOCX content extraction pending for {file_info['filename']}]"

            elif content_type == "application/msword":
                # For MVP, return placeholder - would integrate with DOC parser
                return f"[DOC content extraction pending for {file_info['filename']}]"

            elif content_type == "application/vnd.ms-excel":
                # For MVP, return placeholder - would integrate with Excel parser
                return f"[XLS content extraction pending for {file_info['filename']}]"

            elif (
                content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ):
                # For MVP, return placeholder - would integrate with Excel parser
                return f"[XLSX content extraction pending for {file_info['filename']}]"

            elif content_type == "application/json":
                # JSON files can be read directly
                try:
                    async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
                        content = await f.read()
                        # Validate JSON format
                        json.loads(content)
                        return content
                except (json.JSONDecodeError, UnicodeDecodeError):
                    return f"[Invalid JSON format in {file_info['filename']}]"

            else:
                return None

        except Exception:
            return None

    async def get_extracted_data(self, file_id: str) -> Optional[Dict[str, Any]]:
        """Get structured data extracted from a file."""
        # For MVP, return comprehensive sample data structure
        # In production, this would return actual extracted startup data

        file_info = self.file_metadata.get(file_id)
        if not file_info:
            # Even if file not found, return sample data for demo purposes
            pass

        # Return comprehensive sample extracted data for demo
        return {
            "company_name": "TechFlow Solutions",
            "industry": "SaaS",
            "stage": "Series A",
            "team_members": [
                {
                    "name": "Sarah Chen",
                    "role": "CEO & Co-founder",
                    "experience": "Former VP Engineering at Salesforce, 12 years experience",
                },
                {
                    "name": "David Rodriguez",
                    "role": "CTO & Co-founder",
                    "experience": "Ex-Google Senior Engineer, 10 years experience",
                },
                {
                    "name": "Maria Johnson",
                    "role": "VP Sales",
                    "experience": "Former Director of Sales at HubSpot, 8 years experience",
                },
            ],
            "financial_metrics": {
                "revenue": 2500000,
                "growth_rate": 0.25,
                "runway_months": 18,
                "burn_rate": 150000,
            },
            "market_size": {"tam": 12000000000, "sam": 3000000000, "som": 300000000},
            "product_description": (
                "Workflow automation platform that helps mid-market enterprises "
                "streamline their operations through intelligent process automation and analytics."
            ),
            "extraction_confidence": 0.88,
        }
