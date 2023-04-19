from confluent_kafka.admin import AdminClient
from .controller import Controller
from .error import K4Error

import click
import curses
import yaml
import os
import traceback


@click.command()
@click.version_option(package_name="K4", prog_name="K4")
@click.option(
    "--bootstrap-servers",
    "-b",
    default="localhost:9092",
    metavar="URLS",
    envvar="K4_BOOTSTRAP_SERVERS",
    show_envvar=True,
    help="The Kafka bootstrap servers.",
)
@click.option(
    "kafka_config",
    "--kafka-config",
    "-f",
    metavar="PATH",
    default=None,
    envvar="K4_CONFIG",
    type=click.File("r"),
    help="Path to the Kafka configuration file in YAML format.",
)
@click.option(
    "--log-level",
    "-l",
    type=click.Choice(
        ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"],
        case_sensitive=False,
    ),
    default="NOTSET",
    metavar="LEVEL",
    envvar="K4_LOG_LEVEL",
    show_envvar=True,
    help="The logging level to use for the logger and console handler.",
)
def cli(bootstrap_servers, kafka_config, log_level):
    """A command-line client for Kafka."""

    log_level = log_level
    kafka_admin_client = AdminClient({"bootstrap.servers": bootstrap_servers})

    controller = Controller()
    err = controller.run(kafka_admin_client)

    if err:
        # Display k4 logo
        click.echo(click.style("\n".join(err.LOGO), fg="red", bold=True))
        click.echo(click.style(str(err) + "\n", bold=True))

        # Then display the traceback
        raise err.error
        traceback.print_tb(err.error.__traceback__)
        click.echo(err.traceback)
