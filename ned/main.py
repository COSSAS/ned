import logging
from pprint import pformat

from ned.config import Config
from ned.io.elasticsearch import connect_to_elastic, ship_records_to_elastic
from ned.producer import Producer


def main(type: str, config: Config, to_elastic: bool = False):
    producer = Producer(type=type)
    benign_records, anomalous_records = producer.produce(
        amount=config.AMOUNT_RECORDS, amount_anomalous=config.AMOUNT_ANOMALIES
    )
    all_records = benign_records + anomalous_records
    if to_elastic:
        es_client = connect_to_elastic(
            es_host=config.ES_HOST,
            es_port=config.ES_PORT,
            es_user=config.ES_USER,
            es_password=config.ES_PASSWORD,
        )
        ship_records_to_elastic(
            index=config.ES_INDEX, es_client=es_client, records=all_records
        )
    else:
        logging.info(pformat(all_records))


if __name__ == "__main__":
    config = Config()
    main(type=config.TYPE_RECORDS, config=config)
