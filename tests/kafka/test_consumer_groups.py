import pytest
from unittest.mock import MagicMock, call, patch
from confluent_kafka import ConsumerGroupState, TopicPartition
from kafka_wrapper.consumer_group import ConsumerGroup


def test_group_does_have_topic_assignments(admin_client, kafka_consumer_group):
    with patch(
        "kafka_wrapper.consumer_group.ConsumerGroup.describe"
    ) as mock_kafka_consumer_group_describe:
        group_id = "group1"
        topic_names = ["topic1", "topic2"]

        mock_kafka_consumer_group_describe.return_value = {
            group_id: {
                "members": [
                    {
                        "assignments": [
                            {
                                "topic": topic_names[0],
                            },
                            {
                                "topic": topic_names[1],
                            },
                        ]
                    }
                ]
            }
        }

        results = kafka_consumer_group.has_topic_assignments(group_id, topic_names)
        assert results


def test_group_does_not_have_topic_assignments(admin_client, kafka_consumer_group):
    with patch(
        "kafka_wrapper.consumer_group.ConsumerGroup.describe"
    ) as mock_kafka_consumer_group_describe:
        group_id = "group1"
        topic_names = ["topic1", "topic2"]

        mock_kafka_consumer_group_describe = {
            group_id: {
                "members": [
                    {
                        "assignments": [
                            {
                                "topic": topic_names[0],
                            }
                            # Does not have topic2
                        ]
                    }
                ]
            }
        }
        results = kafka_consumer_group.has_topic_assignments(group_id, topic_names)
        assert not results  # does not have all topics (e.g topic1 and topic2)


def test_consumer_group_list(admin_client, kafka_consumer_group):
    _ = kafka_consumer_group.list()
    admin_client.assert_has_calls(
        [
            call.list_consumer_groups(
                states={ConsumerGroupState.EMPTY, ConsumerGroupState.STABLE}, request_timeout=10
            ),
            call.list_consumer_groups().result(),
            call.list_consumer_groups().result().valid.__iter__(),
        ]
    )

def test_consumer_group_does_exist(admin_client, kafka_consumer_group):
    with patch(
        "kafka_wrapper.consumer_group.ConsumerGroup.list"
    ) as mock_kafka_consumer_group_list:
    
        mock_kafka_consumer_group_list.return_value = [
            {'id': 'group1'},
            {'id': 'group2'},
            {'id': 'group3'}
        ]
        result = kafka_consumer_group.does_exist('group2')
        assert result

def test_consumer_group_does_not_exist(admin_client, kafka_consumer_group):
    with patch(
        "kafka_wrapper.consumer_group.ConsumerGroup.list"
    ) as mock_kafka_consumer_group_list:
    
        mock_kafka_consumer_group_list.return_value = [
            {'id': 'group1'},
            {'id': 'group2'},
            {'id': 'group3'}
        ]
        result = kafka_consumer_group.does_exist('this.group.does.not.exist')
        assert not result


def test_consumer_group_list_only_stable(admin_client, kafka_consumer_group):
    _ = kafka_consumer_group.list(only_stable=True)
    admin_client.assert_has_calls(
        [
            call.list_consumer_groups(states={ConsumerGroupState.STABLE}, request_timeout=10),
            call.list_consumer_groups().result(),
            call.list_consumer_groups().result().valid.__iter__(),
        ]
    )


def test_consumer_group_list_only_high_level(admin_client, kafka_consumer_group):
    _ = kafka_consumer_group.list(only_high_level=True)
    admin_client.assert_has_calls(
        [
            call.list_consumer_groups(
                states={ConsumerGroupState.EMPTY, ConsumerGroupState.STABLE}, request_timeout=10
            ),
            call.list_consumer_groups().result(),
            call.list_consumer_groups().result().valid.__iter__(),
        ]
    )


def test_consumer_group_get_offset_lag(kafka_consumer_group, consumer):
    mock_partitions = [
        MagicMock(topic="topic1", partition=0, offset=10),
        MagicMock(topic="topic1", partition=1, offset=-1),
        MagicMock(topic="topic2", partition=0, offset=100),
    ]
    consumer.committed.return_value = mock_partitions
    consumer.get_watermark_offsets.side_effect = [(0, 100), (0, 200), (50, 200)]

    topic_partitions = [
        TopicPartition("topic1", 0),
        TopicPartition("topic1", 1),
        TopicPartition("topic2", 0),
    ]
    result = kafka_consumer_group.get_offset_lag(topic_partitions, consumer)
    consumer.assert_has_calls(
        [
            call.__bool__(),
            call.committed(topic_partitions, timeout=10),
            call.get_watermark_offsets(mock_partitions[0], timeout=10, cached=False),
            call.get_watermark_offsets(mock_partitions[1], timeout=10, cached=False),
            call.get_watermark_offsets(mock_partitions[2], timeout=10, cached=False),
            call.close(),
        ]
    )


def test_consumer_group_describe(admin_client, kafka_consumer_group):
    group_ids = ["group1", "group2"]
    _ = kafka_consumer_group.describe(group_ids=group_ids)
    admin_client.assert_has_calls(
        [
            call.describe_consumer_groups(group_ids, request_timeout=10),
            call.describe_consumer_groups().items(),
            call.describe_consumer_groups().items().__iter__(),
        ]
    )

def test_consumer_group_describe_wtihout_including_offset_lag(admin_client, kafka_consumer_group):
    group_ids = ["group1", "group2"]
    _ = kafka_consumer_group.describe(group_ids=group_ids, include_offset_lag=False)
    admin_client.assert_has_calls(
        [
            call.describe_consumer_groups(group_ids, request_timeout=10),
            call.describe_consumer_groups().items(),
            call.describe_consumer_groups().items().__iter__(),
        ]
    )


def test_consumer_group_delete(admin_client, kafka_consumer_group):
    group_ids = ["group1", "group2"]
    _ = kafka_consumer_group.delete(group_ids)

    admin_client.assert_has_calls(
        [
            call.delete_consumer_groups(group_ids, request_timeout=10),
            call.delete_consumer_groups().items(),
            call.delete_consumer_groups().items().__iter__(),
        ]
    )
