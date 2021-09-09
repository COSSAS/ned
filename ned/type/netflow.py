import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Collection, Dict

from ned.type.record import Record

suricata_template_netflow = {
    "timestamp": "",  # 2021-01-25T11:03:55.000161+0100
    "flow_id": "0",  # 2113418505840631
    "event_type": "flow",
    "src_ip": "",
    "src_port": "0",
    "dest_ip": "",
    "dest_port": "0",
    "proto": "TCP",
    "app_proto": "dcerpc",
    "flow": {
        "pkts_toserver": "0",
        "pkts_toclient": "0",
        "bytes_toserver": "0",
        "bytes_toclient": "0",
        "start": "",  # 2021-01-25T11:02:53.813047+0100
        "end": "",  # 2021-01-25T11:02:53.831490+0100
        "age": "0",
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
class NetflowRecord(Record):
    flow_id: int
    timestamp: datetime
    suricata: Dict[str, Collection[str]]

    def __post_init__(self) -> None:
        self.suricata["flow_id"] = str(self.flow_id)
        self.suricata["src_ip"] = self.src_ip
        self.suricata["dest_ip"] = self.dest_ip
        self.suricata["flow"]["start"] = self.timestamp.isoformat()  # type: ignore[index]
        self.suricata["flow"]["end"] = (  # type: ignore[index]
            self.timestamp + timedelta(seconds=2)
        ).isoformat()
        self.suricata["timestamp"] = self.timestamp.isoformat()
        self.suricata["pkts_toclient"] = str(random.randint(0, 32))  # nosec
        self.suricata["pkts_toserver"] = str(random.randint(0, 32))  # nosec
        self.suricata["bytes_toclient"] = str(int(self.suricata["pkts_toclient"]) * 8)  # type: ignore[call-overload]
        self.suricata["bytes_toserver"] = str(int(self.suricata["pkts_toserver"]) * 8)  # type: ignore[call-overload]
        self.suricata["src_port"] = str(random.randint(0, 32))  # nosec
        self.suricata["dest_port"] = str(random.randint(0, 32))  # nosec
