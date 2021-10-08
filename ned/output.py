import hashlib
import json
import logging
from pprint import pformat
from typing import Any, Generator

import elasticsearch


def ship_record_to_elastic(
    index: str,
    es_client: elasticsearch.Elasticsearch,
    record: Any,
) -> None:
    es_client.indices.create(index=index, ignore=400)
    record_id = compute_id(record)
    es_client.index(
        index=index,
        ignore=400,
        id=record_id,
        document=json.loads(json.dumps(record.suricata)),
    )
    logging.info("%s %s", record_id, pformat(record.suricata))


def generate_to_elastic(
    es_client: elasticsearch.Elasticsearch,
    generator: Generator[Any, None, None],
    record_type: str,
    es_index: str,
) -> None:
    if record_type == "netflow":
        for record in generator:
            ship_record_to_elastic(
                index=es_index,
                es_client=es_client,
                record=record,
            )
    elif record_type == "dns":
        for request, response in generator:
            ship_record_to_elastic(
                index=es_index,
                es_client=es_client,
                record=request,
            )
            ship_record_to_elastic(
                index=es_index,
                es_client=es_client,
                record=response,
            )


def compute_id(record: Any) -> str:
    concatenated_string = (
        record.suricata["src_ip"] + record.suricata["dest_ip"] + str(record.timestamp)
    )
    return hashlib.md5(bytes(concatenated_string, "utf-8")).hexdigest()  # nosec
