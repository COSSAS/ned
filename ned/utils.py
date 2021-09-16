import logging
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pprint import pformat
from typing import List

import dateutil.parser as dp

from ned.type.record import Record


@dataclass
class Config:
    ES_HOST: str = "localhost"
    ES_PORT: str = "9200"
    ES_INDEX: str = "netflows"
    ES_USER: str = "elastic"
    ES_PASSWORD: str = "changeme"
    TYPE_RECORDS: str = "netflow"
    NED_AMOUNT_RECORDS: int = 10000
    NED_AMOUNT_RECORDS_ANOMALOUS: int = 0
    NED_START_TIMESTAMP_EPOCHS: float = datetime.now().astimezone().timestamp()
    LOG_LEVEL: str = "WARN"
    from_env: bool = True

    def __post_init__(self) -> None:
        """
        parameters are loaded with the following priority:
        1. from environment variables
        2. from defaults/passed at constructor
        """
        if self.from_env:
            self.__set_from_env__()
        configure_logging(loglevel=self.LOG_LEVEL)
        logging.info("configuration: \n%s", pformat(asdict(self)))

    def __set_from_env__(self) -> None:
        self.ES_HOST = os.environ.get("ES_HOST", self.ES_HOST)
        self.ES_PORT = os.environ.get("ES_PORT", self.ES_PORT)
        self.ES_INDEX = os.environ.get("ES_INDEX", self.ES_INDEX)
        self.ES_USER = os.environ.get("ES_USER", self.ES_USER)
        self.ES_PASSWORD = os.environ.get("ES_PASSWORD", self.ES_PASSWORD)
        self.TYPE_RECORDS = os.environ.get("TYPE_RECORDS", self.TYPE_RECORDS)
        self.NED_AMOUNT_RECORDS = int(
            os.environ.get("NED_AMOUNT_RECORDS", self.NED_AMOUNT_RECORDS)
        )
        self.NED_AMOUNT_RECORDS_ANOMALOUS = int(
            os.environ.get(
                "NED_AMOUNT_RECORDS_ANOMALOUS", self.NED_AMOUNT_RECORDS_ANOMALOUS
            )
        )
        self.NED_START_TIMESTAMP_EPOCHS = float(
            os.environ.get(
                "NED_START_TIMESTAMP_EPOCHS", self.NED_START_TIMESTAMP_EPOCHS
            )
        )
        self.LOG_LEVEL = os.environ.get("LOG_LEVEL", self.LOG_LEVEL)


def configure_logging(loglevel: str) -> None:
    logging.basicConfig(
        format="%(levelname)s: %(message)s",
        level=loglevel.upper(),
    )


def log_records_timestamps(records: List[Record], type: str = "benign  ") -> None:
    first_ts = records[0].suricata["timestamp"]
    last_ts = records[-1].suricata["timestamp"]
    logging.warning(
        "start %s records:    %s %s",
        type,
        first_ts,
        int(dp.parse(first_ts).timestamp()),
    )
    logging.warning(
        "end   %s records:    %s %s",
        type,
        last_ts,
        int(dp.parse(last_ts).timestamp()),
    )
