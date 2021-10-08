from ned.main import main
from ned.utils import Config


def test_main_netflows():
    config = Config(
        TYPE_RECORDS="netflow",
        NED_AMOUNT_RECORDS=2,
        NED_AMOUNT_RECORDS_ANOMALOUS=1,
        NED_START_TIMESTAMP_EPOCHS=0,
        LOG_LEVEL="info",
        from_env=False,
    )
    main(record_type=config.TYPE_RECORDS, config=config)
