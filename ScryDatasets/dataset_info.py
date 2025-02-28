
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class DatasetInfo:
    """Data class for dataset information"""
    _id: Optional[str]
    name: str
    createdOn: datetime
    description: Optional[str]
    fileSize: int
    fileName: str
    accessLink: str
    tags: Optional[List[str]] = None