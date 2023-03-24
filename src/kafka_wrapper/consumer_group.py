from confluent_kafka import ConsumerGroupState, Consumer, OFFSET_INVALID
from confluent_kafka import KafkaException, KafkaError
from .kafka_resource import KafkaResource
from .topic import Topic


class ConsumerGroup(KafkaResource):
    def __init__(self, admin_client_config=None, timeout=10, log_level=None):
        """
        The Consumer Group wrapper class.
        Args:
            admin_client_config (dict): The Kafka AdminClient configuration.
            timeout (int): The timeout for kafka operations.
            log_level (str): The logging level to use for the logger and console handler. Defaults to "NOTSET".
        """
        super().__init__(
            admin_client_config=admin_client_config, timeout=timeout, log_level=log_level
        )

    def has_any_topic_assignments(self, group_id, topic_names):
        """
        Checks whether the Consumer Group is assigned to any specified topic names.
        """
        result = False
        groups_metadata = self.describe(group_ids=[group_id])
        md = groups_metadata[group_id]

        for m in md.get("members", []):
            for a in m.get("assignments", []):
                if a.get("topic") in topic_names:
                    result = True
                    break
        
        return result

    def list(self, only_stable=False, only_high_level=False, topics=[]):
        """
        List Kafka Consumer Groups.
        """
        states = set()

        states.add(ConsumerGroupState.STABLE)

        if not only_stable:
            states.add(ConsumerGroupState.EMPTY)

        future = self._admin_client.list_consumer_groups(
            states=states, request_timeout=self._timeout
        )
        groups = future.result()

        consumer_groups = []
        for group in groups.valid:

            if topics and not self.has_any_topic_assignments(group.group_id, topics):
                continue

            if only_high_level and group.is_simple_consumer_group:
                continue

            consumer_groups.append(
                {
                    "id": group.group_id,
                    "type": "simple" if group.is_simple_consumer_group else "high-level",
                    "state": group.state.name,
                }
            )

        return consumer_groups

    def does_exist(self, group_id):
        return any([g for g in self.list() if g["id"] == group_id])

    def create(
        self,
        group_id,
        topic_names,
        partition=None,
        offset=None,
        earliest=False,
        latest=False,
        config={},
        consumer=None,
    ):
        raise NotImplemented

        # TODO move to consume.py

        # if sum([bool(offset), bool(earliest), bool(latest)]) != 1:
        #     raise ValueError("Only one of the 'offset', 'earliest', or 'latest' arguments are allowed.")

        # consumer_config = self._admin_client_config.copy()

        # if not consumer:
        #     # This is a simple consumer group so we can reuse the admin client config.
        #     # Update with a group.id if it is not already set.
        #     if 'group.id' not in consumer_config:
        #         consumer_config['group.id'] = group_id

        #     # The config arg will take precedence over other args
        #     if config:
        #         consumer_config.update(config)

        #     # This consumer will not join the group, but the group.id is required by
        #     # committed() to know which group to get offsets for.
        #     consumer = Consumer(self._admin_client_config)

        # for t in topic_names:

        #     if not partitions:
        #          topics_metadata = self._admin_client.list_topics(timeout=self._timeout).topics

        #     for p in partitions:
        #         consumer.seek(TopicPartition(t, p, offset))

        consumer.subscribe(topics)

    def get_offset_lag(self, topic_partitions, consumer=None):
        result = {}

        if not consumer:
            # TODO will need to revisit this when we add authentication.

            # This consumer will not join the group, but the group.id is required by
            # committed() to know which group to get offsets for.
            consumer_config = {
                "bootstrap.servers": self._admin_client_config["bootstrap.servers"],
                "group.id": "k4",
            }
            consumer = Consumer(consumer_config)

        # Query committed offsets for this group and the given partitions
        committed = consumer.committed(topic_partitions, timeout=self._timeout)

        for partition in committed:
            # Get the partitions low and high watermark offsets.
            (lo, hi) = consumer.get_watermark_offsets(
                partition, timeout=self._timeout, cached=False
            )

            if partition.offset == OFFSET_INVALID:
                current_offset = "-"
            else:
                current_offset = "%d" % (partition.offset)

            if hi < 0:
                lag = "no hwmark"  # Unlikely
            elif partition.offset < 0:
                # No committed offset, show total message count as lag.
                # The actual message count may be lower due to compaction
                # and record deletions.
                lag = "%d" % (hi - lo)
            else:
                lag = "%d" % (hi - partition.offset)

            result[partition.topic] = {}
            result[partition.topic][partition.partition] = {
                "current_offset": current_offset,
                "log_end_offset": hi,
                "lag": lag,
            }

        consumer.close()

        return result

    def describe(self, group_ids=[], include_offset_lag=True):
        if not group_ids:
            group_ids = [group["id"] for group in self.list()]

        future = self._admin_client.describe_consumer_groups(
            group_ids, request_timeout=self._timeout
        )

        results = {}

        # Describe consumer groups
        for group_id, f in future.items():
            group_metadata = f.result()
            members = []
            for m in group_metadata.members:

                topic_partitions = []
                offsets = []
                if m.assignment:

                    for tp in m.assignment.topic_partitions:

                        if include_offset_lag:
                            #
                            offsets = self.get_offset_lag([tp])
                        else:
                            offsets = {}

                        current_offset = (
                            offsets.get(tp.topic, {})
                            .get(tp.partition, {})
                            .get("current_offset", "-")
                        )
                        log_end_offset = (
                            offsets.get(tp.topic, {})
                            .get(tp.partition, {})
                            .get("log_end_offset", "-")
                        )
                        lag = offsets.get(tp.topic, {}).get(tp.partition, {}).get("lag", "-")

                        topic_partitions.append(
                            {
                                "topic": tp.topic,
                                "partition": tp.partition,
                                "current_offset": current_offset,
                                "log_end_offset": log_end_offset,
                                "lag": lag,
                            }
                        )

                member = {
                    "id": m.member_id,
                    "host": m.host,
                    "client_id": m.client_id,
                    "group_instance_id": m.group_instance_id,
                    "assignments": topic_partitions,
                }
                members.append(member)

            results[group_id] = {
                "is_simple_consumer_group": group_metadata.is_simple_consumer_group,
                "state": group_metadata.state.name,
                "partition_assignor": group_metadata.partition_assignor,
                "coordinator": {
                    "id": group_metadata.coordinator.id,
                    "host": group_metadata.coordinator.host,
                    "port": group_metadata.coordinator.port,
                },
                "members": members,
            }

        return results

    def alter(self):
        raise NotImplemented

    def delete(self, group_ids):
        future = self._admin_client.delete_consumer_groups(group_ids, request_timeout=self._timeout)

        for group_id, f in future.items():
            f.result()
