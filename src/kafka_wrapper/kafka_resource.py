from abc import ABC, abstractmethod
from confluent_kafka.admin import AdminClient

import logging


def get_logger(log_level="NOTSET"):
    """Get a logger configured to write to the console.
    Args:
        log_level (str): The logging level to use for the logger and console handler. Defaults to "NOTSET".
    Returns:
        A logger configured to write log messages with a level equal to or higher
        than `log_level` to the console.
    """
    # create logger
    logger = logging.getLogger("k4")
    log_level_number = logging.getLevelName(log_level.upper())
    logger.setLevel(log_level_number)

    # create console handler and set log level
    ch = logging.StreamHandler()
    ch.setLevel(log_level.upper())

    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    return logger


class KafkaResource(ABC):
    """An abstract class for a Kafka resource."""

    def __init__(self, admin_client_config=None, timeout=10, log_level=None):
        """
        Initialize a new instance of the Consumer Group wrapper class.
        Args:
            admin_client_config (dict): The Kafka AdminClient configuration.
            timeout (int): The timeout for kafka operations.
            log_level (str): The logging level to use for the logger and console handler. Defaults to "NOTSET".
        """
        if not admin_client_config:
            admin_client_config = {"bootstrap.servers": "localhost:9092"}

        self._admin_client_config = admin_client_config

        self._admin_client = AdminClient(admin_client_config)
        log_level = "NOTSET" if not log_level else log_level
        self.logger = get_logger(log_level)
        self._timeout = timeout

    @property
    def admin_client(self):
        self._admin_client

    @admin_client.setter
    def admin_client(self, value):
        self._admin_client = value

    @property
    def timeout(self, value):
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        self._timeout = value

    @abstractmethod
    def list(self):
        """List one or many resources."""
        raise NotImplemented

    @abstractmethod
    def create(self):
        """Create one or many resources."""
        raise NotImplemented

    @abstractmethod
    def describe(self):
        """Describe one or many resources."""
        raise NotImplemented

    @abstractmethod
    def alter(self):
        """Alter one or many resources."""
        raise NotImplemented

    @abstractmethod
    def delete(self):
        """Delete one or many resources."""
        raise NotImplemented
