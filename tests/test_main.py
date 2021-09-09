from ned.main import main
from ned.type.netflow import NetflowRecord
from ned.utils import Config


def test_main_netflows():
    config = Config(
        TYPE_RECORDS="netflow",
        AMOUNT_RECORDS=1,
        AMOUNT_ANOMALIES=1,
        LOG_LEVEL="info",
        from_env=False,
    )
    benign, anomalous = main(type=config.TYPE_RECORDS, config=config)
    assert len(benign) == 1
    assert len(anomalous) == 1
    assert type(benign[0]) is NetflowRecord
    assert type(anomalous[0]) is NetflowRecord
