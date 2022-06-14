import copy
import random
from dataclasses import dataclass
from datetime import datetime, timedelta

from ned.templates import (
    suricata_dns_template_request,
    suricata_dns_template_response,
    suricata_template_netflow,
)


@dataclass
class Record:
    src_ip: str
    flow_id: int
    timestamp: datetime


@dataclass
class NetflowRecord(Record):
    flow_id: int
    timestamp: datetime
    dest_ip: str

    def __post_init__(self) -> None:
        self.suricata = copy.deepcopy(suricata_template_netflow)
        self.suricata["flow_id"] = self.flow_id
        self.suricata["src_ip"] = self.src_ip
        self.suricata["dest_ip"] = self.dest_ip
        self.suricata["flow"]["start"] = self.timestamp.isoformat()  # type: ignore[index]
        self.suricata["flow"]["end"] = (  # type: ignore[index]
            self.timestamp + timedelta(seconds=2)
        ).isoformat()
        self.suricata["timestamp"] = self.timestamp.isoformat()
        self.suricata["flow"]["pkts_toclient"] = random.randint(0, 32)  # type: ignore[index]
        self.suricata["flow"]["pkts_toserver"] = random.randint(0, 32)  # type: ignore[index]
        self.suricata["flow"]["bytes_toclient"] = int(self.suricata["flow"]["pkts_toclient"]) * 8  # type: ignore[index]
        self.suricata["flow"]["bytes_toserver"] = int(self.suricata["flow"]["pkts_toserver"]) * 8  # type: ignore[index]
        self.suricata["src_port"] = random.randint(0, 32)  # nosec
        self.suricata["dest_port"] = random.randint(0, 32)  # nosec


@dataclass
class DNSRecordRequest(Record):
    flow_id: int
    timestamp: datetime
    domain_name: str

    def __post_init__(self) -> None:
        self.suricata = copy.deepcopy(suricata_dns_template_request)
        self.suricata["timestamp"] = self.timestamp.isoformat()
        self.suricata["flow_id"] = self.flow_id
        self.suricata["src_ip"] = self.src_ip
        self.suricata["src_port"] = random.randint(0, 32)  # nosec
        self.suricata["dest_ip"] = "1.1.1.1"
        self.suricata["dest_port"] = 53
        self.suricata["dns"]["rrname"] = self.domain_name  # type: ignore[index]


@dataclass
class DNSRecordResponse(Record):
    flow_id: int
    timestamp: datetime
    domain_name: str

    def __post_init__(self) -> None:
        self.suricata = copy.deepcopy(suricata_dns_template_response)
        self.suricata["timestamp"] = self.timestamp.isoformat()
        self.suricata["flow_id"] = self.flow_id
        self.suricata["src_ip"] = "1.1.1.1"
        self.suricata["src_port"] = 53
        self.suricata["dest_ip"] = self.src_ip
        self.suricata["dest_port"] = random.randint(0, 32)  # nosec
        self.suricata["dns"]["rrname"] = self.domain_name  # type: ignore[index]
        self.suricata["dns"]["answers"][0]["rrname"] = self.domain_name  # type: ignore[index]
        self.suricata["dns"]["answers"][0]["rdata"] = self.domain_name  # type: ignore[index]
        self.suricata["dns"]["grouped"]["A"] = [  # type: ignore[index]
            ".".join(str(random.randint(0, 255)) for _ in range(4))
        ]
        self.suricata["dns"]["grouped"]["CNAME"] = [self.domain_name]  # type: ignore[index]
