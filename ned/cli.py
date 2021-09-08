import click

from ned.config import Config
from ned.main import main


@click.command()
@click.option("--type", required=True, help="data type of record to produce")
@click.option(
    "--to_elastic",
    default=False,
    type=bool,
    help="to send data to elasticsearch",
    show_default=True,
)
def produce(type: str, to_elastic: bool):
    config = Config()
    main(type=type, config=config, to_elastic=to_elastic)


if __name__ == "__main__":
    produce()
