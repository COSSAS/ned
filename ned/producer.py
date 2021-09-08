import logging
import random
import sys
from datetime import datetime, time, timedelta, timezone
from typing import List, Tuple

import dateutil.parser as dp

from ned.type.netflow import NetflowRecord


class Producer:
    def __init__(self, type: str):
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

    def pick_source_ip(self):
        return random.choice(self.hosts_subnet1)

    def pick_destination_ip(self, src_ip: str, anomalous=False):
        if anomalous:
            # anomalous = to another subnet
            return random.choice(self.hosts_subnet2)
        # not anomalous = same subnet, different address
        destinations = self.hosts_subnet1[:]
        destinations.remove(src_ip)
        return random.choice(destinations)

    def produce_one(self, anomalous=False):
        src_ip = self.pick_source_ip()
        dest_ip = self.pick_destination_ip(src_ip=src_ip, anomalous=anomalous)
        if self.type == "netflow":
            record = NetflowRecord(
                flow_id=self.counter,
                src_ip=src_ip,
                dest_ip=dest_ip,
                timestamp=datetime.now(timezone.utc).astimezone()
                + timedelta(seconds=self.counter),
            )
            self.counter += 1
            return record

    def produce_many(self, amount: int = 10000, anomalous: bool = False):
        return [self.produce_one(anomalous=anomalous) for _ in range(amount)]

    def produce(
        self, amount: int, amount_anomalous: int = 0
    ) -> Tuple[List[NetflowRecord], List[NetflowRecord]]:
        benign_records = self.produce_many(amount=amount)
        logging.warn(
            "start benign records:    %s %s",
            benign_records[0].timestamp,
            int(dp.parse(benign_records[0].timestamp).timestamp()),
        )
        logging.warn(
            "end benign records:      %s %s",
            benign_records[-1].timestamp,
            int(dp.parse(benign_records[-1].timestamp).timestamp()),
        )
        anomalous_records = self.produce_many(amount=amount_anomalous, anomalous=True)
        logging.warn(
            "start anomalous records: %s %s",
            anomalous_records[0].timestamp,
            int(dp.parse(anomalous_records[0].timestamp).timestamp()),
        )
        logging.warn(
            "end anomalous records:   %s %s",
            anomalous_records[-1].timestamp,
            int(dp.parse(anomalous_records[-1].timestamp).timestamp()),
        )
        return benign_records, anomalous_records
