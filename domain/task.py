from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Task:
    """
    Task Entity
    """
    id: str
    name: str
    description: str
    status: str
    log: List[str] = None
    result: Optional[str] = None

    def __post_init__(self):
        if self.log is None:
            self.log = []