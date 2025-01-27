
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class DatasetInfo:
    """Data class for dataset information"""
    _id: str
    name: str
    created_at: datetime
    description: Optional[str]
    size_bytes: int
    filename: str
    tags: Optional[List[str]] = None