import hashlib
import json
import logging
import time
from pprint import pformat
from typing import List

import elasticsearch
from elasticsearch import Elasticsearch

from ned.type.record import Record


def connect_to_elastic(
    es_host: str = "localhost",
    es_port: str = "9200",
    es_user: str = "",
    es_password: str = "",
) -> elasticsearch.Elasticsearch:
    connected = False
    while not connected:
        try:
            if es_user and es_password:
                es_client = elasticsearch.Elasticsearch(
                    [
                        f"http://{es_user}:{es_password}@{es_host}:{es_port}/",
                        f"https://{es_user}:{es_password}@{es_host}:{es_port}/",
                    ]
                )
            else:
                es_client = elasticsearch.Elasticsearch(
                    [f"http://{es_host}:{es_port}/", f"https://{es_host}:{es_port}/"]
                )
            logging.info(es_client.info())
            connected = True
        except elasticsearch.exceptions.ConnectionError:
            logging.error("can't reach elasticsearch at %s, retrying...", es_host)
            time.sleep(2)
    return es_client


def ship_records_to_elastic(
    index: str, es_client: elasticsearch.Elasticsearch, records: List[Record]
) -> None:
    es_client.indices.create(index=index, ignore=400)
    for record in records:
        record_id = compute_id(record)
        es_client.index(
            index=index,
            ignore=400,
            id=record_id,
            body=json.loads(json.dumps(record.suricata)),
        )
        logging.info("%s %s", record_id, pformat(record.suricata))


def compute_id(record: Record) -> str:
    concatenated_string = record.src_ip + record.dest_ip + str(record.timestamp)
    return hashlib.md5(bytes(concatenated_string, "utf-8")).hexdigest()  # md5
