from ned.main import main
from ned.type.netflow import NetflowRecord
from ned.utils import Config


def test_main_netflows():
    config = Config(
        TYPE_RECORDS="netflow",
        NED_AMOUNT_RECORDS=1,
        NED_AMOUNT_RECORDS_ANOMALOUS=1,
        LOG_LEVEL="info",
        from_env=False,
    )
    benign, anomalous = main(type=config.TYPE_RECORDS, config=config)
    assert len(benign) == 1
    assert len(anomalous) == 1
    assert type(benign[0]) is NetflowRecord
    assert type(anomalous[0]) is NetflowRecord
