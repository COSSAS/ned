import json
import logging
import time
from typing import List

import elasticsearch


def connect_to_elastic(
    es_host="localhost", es_port=9200, es_user=None, es_password=None
):
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
    index: str, es_client: elasticsearch.Elasticsearch, records: List
) -> None:
    es_client.indices.create(index=index, ignore=400)
    for record in records:
        logging.info(json.dumps(record))
        es_client.index(
            index=index, ignore=400, body=json.loads(json.dumps(record.suricata_entry))
        )
