import logging
import random
import sys
from datetime import datetime, timedelta, timezone
from typing import List, Tuple

from ned.type.netflow import NetflowRecord, suricata_template_netflow
from ned.type.record import Record


class Producer:
    def __init__(
        self,
        type: str,
        start_timestamp_epochs: float = datetime.now().astimezone().timestamp(),
    ):
        self.start_timestamp = datetime.fromtimestamp(
            start_timestamp_epochs
        ).astimezone()
        if type not in ["netflow", "dns"]:
            logging.critical("type must be either 'dns' or 'netflow'")
            sys.exit(1)
        self.type = type
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

    def produce_one(self, timestamp: datetime, anomalous: bool = False) -> Record:
        source_subnet, dest_subnet = self.pick_source_and_dest_subnets(
            anomalous=anomalous
        )
        src_ip = self.pick_source_ip(subnet=source_subnet)
        dest_ip = self.pick_destination_ip(
            src_ip=src_ip, destination_subnet=dest_subnet
        )
        if self.type == "netflow":
            record = NetflowRecord(
                flow_id=self.counter,
                src_ip=src_ip,
                dest_ip=dest_ip,
                timestamp=timestamp,
                suricata=suricata_template_netflow.copy(),
            )
        self.counter += 1
        return record

    def produce_many(
        self, amount: int = 10000, anomalous: bool = False
    ) -> List[Record]:
        return [
            self.produce_one(
                timestamp=self.start_timestamp + timedelta(seconds=self.counter),
                anomalous=anomalous,
            )
            for _ in range(amount)
        ]

    def produce(
        self, amount: int, NED_AMOUNT_RECORDS_ANOMALOUS: int = 0
    ) -> Tuple[List[Record], List[Record]]:
        benign_records = self.produce_many(amount=amount)
        anomalous_records = self.produce_many(
            amount=NED_AMOUNT_RECORDS_ANOMALOUS, anomalous=True
        )
        return benign_records, anomalous_records
