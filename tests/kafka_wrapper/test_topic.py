import pytest
from unittest.mock import MagicMock, call
from confluent_kafka.admin import NewTopic, ConfigResource, ResourceType
from confluent_kafka import KafkaException


def test_topic_list(admin_client, kafka_topic):
    result = kafka_topic.list()
    admin_client.assert_has_calls(
        [
            call.list_topics(timeout=10),
            call.list_topics().topics.values(),
            call.list_topics().topics.values().__iter__(),
        ]
    )


def test_topic_list_without_internal(admin_client, kafka_topic):
    result = kafka_topic.list(show_internal=False)
    admin_client.assert_has_calls(
        [
            call.list_topics(timeout=10),
            call.list_topics().topics.values(),
            call.list_topics().topics.values().__iter__(),
        ]
    )


def test_topic_create(admin_client, kafka_topic):
    topic_name = "topic"
    num_partitions = 3
    replication_factor = 3
    config = {"cleanup.policy": "compact"}

    _ = kafka_topic.create(topic_name, num_partitions, replication_factor, config)

    admin_client.assert_has_calls(
        [
            call.create_topics(
                [
                    NewTopic(
                        topic=topic_name,
                        num_partitions=num_partitions,
                        replication_factor=replication_factor,
                        config=config,
                    )
                ],
                request_timeout=10,
            ),
            call.create_topics().items(),
            call.create_topics().items().__iter__(),
        ]
    )


def test_topic_describe(admin_client, kafka_topic):
    _ = kafka_topic.describe(topic_names=["topic1", "topic2"])

    admin_client.assert_has_calls(
        [
            call.list_topics(timeout=10),
            call.list_topics().topics.items(),
            call.list_topics().topics.items().__iter__(),
        ]
    )

    # assert that list_topics is called when the topics argument is not specified
    _ = kafka_topic.describe()

    admin_client.assert_has_calls(
        [
            call.list_topics(timeout=10),
            call.list_topics().topics.items(),
            call.list_topics().topics.items().__iter__(),
        ]
    )


def test_topic_describe_configs(admin_client, kafka_topic):
    admin_client.list_topics.return_value = MagicMock(
        topics={topic: {} for topic in ["topic1", "topic2"]}
    )
    admin_client.describe_configs.return_value = MagicMock()

    _ = kafka_topic.describe_configs()

    admin_client.assert_has_calls(
        [
            call.list_topics(timeout=10),
            call.describe_configs(
                [
                    ConfigResource(ResourceType.TOPIC, "topic1"),
                    ConfigResource(ResourceType.TOPIC, "topic2"),
                ]
            ),
            call.describe_configs().items(),
            call.describe_configs().items().__iter__(),
        ]
    )


def test_topic_describe_configs_with_does_not_exist_side_effect(admin_client, kafka_topic):
    with pytest.raises(ValueError):
        _ = kafka_topic.describe_configs(topic_names=["topic1", "topic2"])


def test_topic_alter(admin_client, kafka_topic):
    topic_name = "topic1"
    config = {"cleanup.policy": "compact"}
    topics = _ = kafka_topic.alter(topic_name, config=config)

    admin_client.assert_has_calls(
        [
            call.alter_configs([ConfigResource(ResourceType.TOPIC, topic_name)]),
            call.alter_configs().items(),
            call.alter_configs().items().__iter__(),
        ]
    )


def test_topic_delete(admin_client, kafka_topic):
    topic_names = ["topic1", "topic2"]
    _ = kafka_topic.delete(topic_names)

    admin_client.assert_has_calls(
        [
            call.delete_topics(topic_names, operation_timeout=10),
            call.delete_topics().items(),
            call.delete_topics().items().__iter__(),
        ]
    )
