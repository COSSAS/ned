import dataclasses
import random
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

suricata_dict_template = {
    "timestamp": "",  # 2021-01-25T11:03:55.000161+0100
    "flow_id": 0,  # 2113418505840631
    "event_type": "flow",
    "src_ip": "",
    "src_port": 0,
    "dest_ip": "",
    "dest_port": 0,
    "proto": "TCP",
    "app_proto": "dcerpc",
    "flow": {
        "pkts_toserver": 0,
        "pkts_toclient": 0,
        "bytes_toserver": 0,
        "bytes_toclient": 0,
        "start": "",  # 2021-01-25T11:02:53.813047+0100
        "end": "",  # 2021-01-25T11:02:53.831490+0100
        "age": 0,
        "state": "established",
        "reason": "timeout",
        "alerted": "false",
    },
    "tcp": {
        "tcp_flags": "da",
        "tcp_flags_ts": "da",
        "tcp_flags_tc": "5a",
        "syn": "true",
        "psh": "true",
        "ack": "true",
        "ecn": "true",
        "cwr": "true",
        "state": "established",
    },
}


@dataclass
class NetflowRecord:
    flow_id: int
    src_ip: str
    dest_ip: str
    src_port: int = random.randint(0, 65535)
    dest_port: int = random.randint(0, 65535)
    timestamp: datetime = datetime.now(timezone.utc).astimezone()
    pkts_toserver: int = random.randint(0, 32)
    pkts_toclient: int = random.randint(0, 32)
    bytes_toserver: int = 8 * random.randint(0, 32)
    bytes_toclient: int = 8 * random.randint(0, 32)
    flow_start: Optional[datetime] = None
    flow_end: Optional[datetime] = None
    suricata_entry: Optional[dict] = dataclasses.field(default_factory=dict)

    def __post_init__(self):
        self.flow_end = (self.timestamp + timedelta(seconds=2)).isoformat()
        self.flow_start = self.timestamp.isoformat()
        self.timestamp = self.timestamp.isoformat()
        self.suricata_entry = suricata_dict_template
        self.suricata_entry["timestamp"] = self.timestamp
        self.suricata_entry["flow"]["start"] = self.flow_start
        self.suricata_entry["flow"]["end"] = self.flow_end
        self.suricata_entry["flow_id"] = self.flow_id
        self.suricata_entry["src_ip"] = self.src_ip
        self.suricata_entry["dest_ip"] = self.dest_ip
        self.suricata_entry["src_port"] = self.src_port
        self.suricata_entry["dest_port"] = self.dest_port
        self.suricata_entry["pkts_toserver"] = self.pkts_toserver
        self.suricata_entry["pkts_toclient"] = self.pkts_toclient
        self.suricata_entry["bytes_toserver"] = self.bytes_toserver
        self.suricata_entry["bytes_toclient"] = self.bytes_toclient
