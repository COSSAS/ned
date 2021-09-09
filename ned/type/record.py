from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict


@dataclass
class Record:
    src_ip: str
    dest_ip: str
    timestamp: datetime
    suricata: Dict[str, Any]
