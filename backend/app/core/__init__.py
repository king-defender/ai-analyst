"""Core configuration and utilities"""

from .config import Settings

# Create global settings instance
settings = Settings()

__all__ = ["Settings", "settings"]
