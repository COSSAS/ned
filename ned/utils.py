import logging
import os
from dataclasses import asdict, dataclass
from pprint import pformat
from typing import List

import dateutil.parser as dp


@dataclass
class Config:
    ES_HOST: str = "localhost"
    ES_PORT: str = "9200"
    ES_INDEX: str = "netflows"
    ES_USER: str = "elastic"
    ES_PASSWORD: str = "changeme"
    TYPE_RECORDS: str = "netflow"
    AMOUNT_RECORDS: int = 10000
    AMOUNT_ANOMALIES: int = 5
    LOG_LEVEL: str = "WARN"
    from_env: bool = True

    def __post_init__(self):
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
        self.AMOUNT_RECORDS = os.environ.get("AMOUNT_RECORDS", self.AMOUNT_RECORDS)
        self.AMOUNT_ANOMALIES = os.environ.get(
            "AMOUNT_ANOMALIES", self.AMOUNT_ANOMALIES
        )
        self.LOG_LEVEL = os.environ.get("LOG_LEVEL", self.LOG_LEVEL)


def configure_logging(loglevel: str) -> None:
    logging.basicConfig(
        format="%(levelname)s: %(message)s",
        level=loglevel.upper(),
    )


def log_records_timestamps(records: List, type: str = "benign  ") -> None:
    logging.warn(
        "start %s records:    %s %s",
        type,
        records[0].timestamp,
        int(dp.parse(records[0].timestamp).timestamp()),
    )
    logging.warn(
        "end   %s records:    %s %s",
        type,
        records[-1].timestamp,
        int(dp.parse(records[-1].timestamp).timestamp()),
    )
