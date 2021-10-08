import logging
import random
import string
import sys
from datetime import datetime, timedelta
from importlib import resources
from typing import Any, Generator, List, Tuple

import ned.utils
from ned.records import DNSRecordRequest, DNSRecordResponse, NetflowRecord, Record


class Producer:
    def __init__(
        self,
        record_type: str,
        start_timestamp_epochs: float = datetime.now().astimezone().timestamp(),
    ):
        self.start_timestamp = datetime.fromtimestamp(
            start_timestamp_epochs
        ).astimezone()
        if record_type not in ["netflow", "dns"]:
            logging.critical("record type must be either 'dns' or 'netflow'")
            sys.exit(1)
        self.record_type = record_type
        self.counter: int = 0
        self.hosts_subnet1 = [
            "10.0.0.1",
            "10.0.0.2",
            "10.0.0.3",
            "10.0.0.4",
            "10.0.0.5",
        ]
        self.hosts_subnet2 = [
            "192.168.0.1",
            "192.168.0.2",
            "192.168.0.3",
            "192.168.0.4",
            "192.168.0.5",
        ]

    def pick_source_and_dest_subnets(
        self,
        anomalous: bool = False,
    ) -> Tuple[List[str], List[str]]:
        if self.counter % 2 == 0:
            source_subnet = self.hosts_subnet1[:]
        else:
            source_subnet = self.hosts_subnet2[:]

        if not anomalous:
            dest_subnet = source_subnet[:]
        elif self.counter % 2 == 0:
            dest_subnet = self.hosts_subnet2[:]
        else:
            dest_subnet = self.hosts_subnet1[:]
        return source_subnet, dest_subnet

    def pick_source_ip(self, subnet: List[str]) -> str:
        return random.choice(subnet)  # nosec

    def pick_destination_ip(self, src_ip: str, destination_subnet: List[str]) -> str:
        if src_ip in destination_subnet:
            destination_subnet.remove(src_ip)
        return random.choice(destination_subnet)  # nosec

    def produce_one_netflow(
        self, timestamp: datetime, anomalous: bool = False
    ) -> Record:
        source_subnet, dest_subnet = self.pick_source_and_dest_subnets(
            anomalous=anomalous
        )
        src_ip = self.pick_source_ip(subnet=source_subnet)
        dest_ip = self.pick_destination_ip(
            src_ip=src_ip, destination_subnet=dest_subnet
        )
        record = NetflowRecord(
            flow_id=self.counter, src_ip=src_ip, dest_ip=dest_ip, timestamp=timestamp
        )
        self.counter += 1
        return record

    def produce_one_dns_pair(
        self, timestamp: datetime, anomalous: bool = False
    ) -> Tuple[DNSRecordRequest, DNSRecordResponse]:
        src_ip = self.pick_source_ip(subnet=self.hosts_subnet1)
        if anomalous:
            domain_name = (
                "".join(
                    random.choice(string.ascii_lowercase)
                    for _ in range(random.randint(10, 30))
                )
                + ".com"
            )
        else:
            with resources.path(ned, "top-1000-domains.txt") as top_domains_filepath:
                domain_name = random.choice(list(open(top_domains_filepath))).rstrip()
        request = DNSRecordRequest(
            src_ip=src_ip,
            flow_id=self.counter,
            timestamp=timestamp,
            domain_name=domain_name,
        )
        response = DNSRecordResponse(
            src_ip=src_ip,
            flow_id=self.counter,
            timestamp=timestamp,
            domain_name=domain_name,
        )
        self.counter += 1
        return request, response

    def generate_records(self, amount: int, anomalous: bool = False) -> Any:
        for _ in range(amount):
            if self.record_type == "netflow":
                yield self.produce_one_netflow(
                    timestamp=self.start_timestamp + timedelta(seconds=self.counter),
                    anomalous=anomalous,
                )
            elif self.record_type == "dns":
                yield self.produce_one_dns_pair(
                    timestamp=self.start_timestamp + timedelta(seconds=self.counter),
                    anomalous=anomalous,
                )
