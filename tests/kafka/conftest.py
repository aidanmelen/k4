from unittest.mock import MagicMock
from kafka_wrapper.broker import Broker
from kafka_wrapper.topic import Topic
from kafka_wrapper.consumer_group import ConsumerGroup

import pytest


@pytest.fixture
def admin_client():
    return MagicMock()


@pytest.fixture
def consumer():
    return MagicMock()


@pytest.fixture
def kafka_broker(admin_client):
    b = Broker({"bootstrap.servers": "mock:9092"})
    b.admin_client = admin_client
    return b


@pytest.fixture
def kafka_topic(admin_client):
    t = Topic({"bootstrap.servers": "mock:9092"})
    t.admin_client = admin_client
    return t


@pytest.fixture
def kafka_consumer_group(admin_client):
    g = ConsumerGroup({"bootstrap.servers": "mock:9092"})
    g.admin_client = admin_client
    return g
