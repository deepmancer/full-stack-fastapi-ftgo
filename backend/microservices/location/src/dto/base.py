from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class BaseDTO:
    created_at: Optional[datetime] = None

    def to_dict(self):
        return asdict(self)
