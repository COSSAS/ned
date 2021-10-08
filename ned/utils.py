import logging
import os
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from distutils.util import strtobool
from pprint import pformat

import elasticsearch
from elasticsearch import Elasticsearch


@dataclass
class Config:
    ES_HOST: str = "localhost"
    ES_PORT: str = "9200"
    ES_INDEX: str = "netflows"
    ES_USER: str = "elastic"
    ES_PASSWORD: str = "changeme"
    ES_USE_SSL: bool = False
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
        if "ES_USE_SSL" in os.environ:
            self.ES_USE_SSL = strtobool(os.environ["ES_USE_SSL"])
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


def connect_to_elastic(  # nosec
    es_host: str = "localhost",
    es_port: str = "9200",
    es_user: str = "",
    es_password: str = "",
    use_ssl: bool = False,
) -> elasticsearch.Elasticsearch:
    connected = False
    if use_ssl:
        es_client = Elasticsearch(
            f"https://{es_user}:{es_password}@{es_host}:{es_port}",
            use_ssl=True,
            verify_certs=False,
            ssl_show_warn=False,
        )
    elif es_user and es_password:
        es_client = Elasticsearch(f"http://{es_user}:{es_password}@{es_host}:{es_port}")
    else:
        es_client = Elasticsearch(f"http://{es_host}:{es_port}")
    while not connected:
        try:
            logging.info(es_client.info())
            connected = True
        except elasticsearch.exceptions.ConnectionError:
            logging.error("can't reach elasticsearch at %s, retrying...", es_host)
            time.sleep(2)
    return es_client
