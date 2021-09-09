from dataclasses import dataclass
from datetime import datetime

@dataclass
class Record:
    src_ip: str
    dest_ip: str
    timestamp: datetime
