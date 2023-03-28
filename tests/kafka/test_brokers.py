import pytest
from unittest.mock import MagicMock, call
from confluent_kafka.admin import ConfigResource, ResourceType
from confluent_kafka import ConsumerGroupState


def test_broker_list(admin_client, kafka_broker):
    _ = kafka_broker.list()
    admin_client.assert_has_calls(
        [
            call.list_topics(timeout=10),
            call.list_topics().brokers.items(),
            call.list_topics().brokers.items().__iter__(),
        ]
    )


def test_broker_describe(admin_client, kafka_broker, kafka_consumer_group):
    _ = kafka_broker.describe(consumer_group=kafka_consumer_group)
    admin_client.assert_has_calls(
        [
            call.list_topics(timeout=10),
            call.list_topics().topics.items(),
            call.list_topics().topics.items().__iter__(),
            call.list_consumer_groups(states={ConsumerGroupState.STABLE}, request_timeout=10),
            call.list_consumer_groups().result(),
            call.list_consumer_groups().result().valid.__iter__(),
            call.list_topics().brokers.values(),
            call.list_topics().brokers.values().__len__(),
        ]
    )


def test_broker_describe_configs(admin_client, kafka_broker):
    _ = kafka_broker.describe_configs(broker_id="1")
    assert admin_client.describe_configs.called
    # admin_client.assert_has_calls(
    #     [
    #         call.describe_configs([ConfigResource(ResourceType.BROKER,1)], request_timeout=10),
    #         call.describe_configs().items(),
    #         call.describe_configs().items().__iter__(),
    #         call.describe_configs.__bool__()
    #     ]
    # )


def test_broker_describe_config_with_controller(admin_client, kafka_broker):
    # mock_controller_id = "2"
    # mock_topic_metadata = MagicMock()
    # mock_topic_metadata.controller_id = mock_controller_id
    # admin_client.list_topics.return_value = mock_topic_metadata
    _ = kafka_broker.describe_configs()
    assert admin_client.list_topics.called
    assert admin_client.describe_configs.called
    # admin_client.assert_has_calls(
    #     [
    #         call.list_topics(timeout=11),
    #         call.describe_configs([ConfigResource(ResourceType.BROKER, mock_controller_id)], request_timeout=10),
    #         call.describe_configs().items(),
    #         call.describe_configs().items().__iter__()
    #     ]
    # )


def test_broker_alter(admin_client, kafka_broker):
    config = {"auto.create.topics.enable": "false"}
    topics = _ = kafka_broker.alter(config)

    admin_client.assert_has_calls(
        [
            call.list_topics(timeout=10),
            call.list_topics().brokers.items(),
            call.list_topics().brokers.items().__iter__(),
        ]
    )


def test_broker_alter_with_broker_ids(admin_client, kafka_broker):
    broker_id = "1"
    config = {"auto.create.topics.enable": "false"}
    topics = _ = kafka_broker.alter(config, broker_ids=[broker_id])

    admin_client.assert_has_calls(
        [
            call.alter_configs([ConfigResource(ResourceType.BROKER, broker_id)]),
            call.alter_configs().items(),
            call.alter_configs().items().__iter__(),
        ]
    )
