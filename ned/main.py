import logging
from pprint import pformat

from ned.output import generate_to_elastic
from ned.producer import Producer
from ned.utils import Config, connect_to_elastic


def main(record_type: str, config: Config, to_elastic: bool = False) -> None:
    producer = Producer(
        record_type=record_type,
        start_timestamp_epochs=config.NED_START_TIMESTAMP_EPOCHS,
    )
    benign_records_generator = producer.generate_records(
        amount=config.NED_AMOUNT_RECORDS, anomalous=False
    )
    anomalous_records_generator = producer.generate_records(
        amount=config.NED_AMOUNT_RECORDS_ANOMALOUS, anomalous=True
    )
    if not to_elastic:
        for record in benign_records_generator:
            logging.info(pformat(record))
        for record in anomalous_records_generator:
            logging.info(pformat(record))
    else:
        es_client = connect_to_elastic(
            es_host=config.ES_HOST,
            es_port=config.ES_PORT,
            es_user=config.ES_USER,
            es_password=config.ES_PASSWORD,
            use_ssl=config.ES_USE_SSL,
        )
        generate_to_elastic(
            es_client, benign_records_generator, record_type, config.ES_INDEX
        )
        generate_to_elastic(
            es_client, anomalous_records_generator, record_type, config.ES_INDEX
        )


if __name__ == "__main__":
    config = Config(LOG_LEVEL="INFO")
    main(record_type=config.TYPE_RECORDS, config=config)
