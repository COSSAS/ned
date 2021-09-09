import click

from ned.main import main
from ned.utils import Config


@click.command()
@click.option("--type", required=True, help="data type of record to produce")
@click.option(
    "--to-elastic",
    is_flag=True,
    help="to send data to elasticsearch",
    show_default=True,
)
def produce(type: str, to_elastic: bool):
    config = Config()
    main(type=type, config=config, to_elastic=to_elastic)
