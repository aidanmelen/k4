from confluent_kafka.admin import NewTopic, ConfigResource
from .kafka_resource import KafkaResource


class Topic(KafkaResource):
    def __init__(self, admin_client_config=None, timeout=10, log_level=None):
        """
        The Kafka Topic wrapper class.

        Args:
            admin_client_config (dict): The Kafka AdminClient configuration.
            timeout (int): The timeout for kafka operations.
            log_level (str): The logging level to use for the logger and console handler. Defaults to "NOTSET".
        """
        super().__init__(
            admin_client_config=admin_client_config, timeout=timeout, log_level=log_level
        )

    def __str__(self):
        return "Topic"

    def list(self, show_internal=True):
        topics_metadata = self._admin_client.list_topics(timeout=self._timeout)

        results = [
            {
                "name": str(topic),
                "partitions": len(topic.partitions),
            }
            for topic in topics_metadata.topics.values()
        ]

        if not show_internal:
            results = [
                t
                for t in results
                if not (
                    t["name"].startswith("__") or t["name"].startswith("_confluent") 
                    or (t["name"].startswith("connect-") and t["name"].endswith("-offsets"))
                    or (t["name"].startswith("connect-") and t["name"].endswith("-configs"))
                    or (t["name"].startswith("connect-") and t["name"].endswith("-status"))
                    or (t["name"] == "schemas")
                )
            ]

        return results

    def does_exist(self, topic_name):
        return any([t for t in self.list() if t["name"] == topic_name])

    def create(self, topic_name, num_partitions, replication_factor, config={}):
        new_topic = NewTopic(
            topic_name,
            num_partitions=num_partitions,
            replication_factor=replication_factor,
            config=config,
        )
        future = self._admin_client.create_topics([new_topic], request_timeout=self._timeout)

        for topic, f in future.items():
            return f.result()

    def describe(self, topic_names=[]):

        # List all topics metadata when the topics argument is not set
        if topic_names:
            topics_metadata = {
                topic_name: metadata
                for topic_name, metadata in self._admin_client.list_topics(
                    timeout=self._timeout
                ).topics.items()
                if topic_name in topic_names
            }
        else:
            topics_metadata = self._admin_client.list_topics(timeout=self._timeout).topics

        # Get topic description(s)
        results = {}
        for topic_name, topic_metadata in topics_metadata.items():
            results[topic_name] = {}
            partitions = []

            # Loop over all partitions of this topic.
            for partition in topic_metadata.partitions.values():
                replicas = []
                isrs = []
                status = []

                # Loop over all replicas of this partition.
                for broker in partition.replicas:
                    if isinstance(broker, int):
                        replicas.append(broker)
                    else:
                        replicas.append(broker.id)

                # Loop over all in-sync replicas of this partition.
                for broker in partition.isrs:
                    if isinstance(broker, int):
                        isrs.append(broker)
                    else:
                        isrs.append(broker.id)

                partitions.append(
                    {
                        "id": partition.id,
                        "leader": partition.leader,
                        "replicas": replicas,
                        "isrs": isrs,
                        "status": "HEALTHY" if len(isrs) == len(replicas) else "UNDER-REPLICATED",
                    }
                )

            results[topic_name]["partitions"] = len(partitions)
            results[topic_name]["replicas"] = len(replicas)
            results[topic_name]["availability"] = partitions

        return results

    def describe_configs(self, topic_names=[]):
        """
        Describe one or many Kafka Topic configurations.
        """
        results = {}

        if topic_names:
            # assert the topics exists
            response_metadata = {
                topic: metadata
                for topic, metadata in self._admin_client.list_topics(
                    timeout=self._timeout
                ).topics.items()
                if topic in topic_names
            }
        else:
            response_metadata = self._admin_client.list_topics(timeout=self._timeout).topics

        # Get the topic config(s)
        resources = [ConfigResource("topic", t) for t in response_metadata.keys()]
        if not resources:
            err_msg = "Expected at least one topic to be described."
            if topic_names:
                err_msg += f" The provided topics did not exist: {', '.join(topic_names)}"
            raise ValueError(err_msg)

        future = self._admin_client.describe_configs(resources)
        for topic, f in future.items():
            response_metadata = f.result()
            results[topic.name] = {}
            results[topic.name] = {
                m.name: m.value if m.value != "" and m.value != None else "-"
                for m in response_metadata.values()
            }

        return results

    def alter(self, topic_name, config, overwrite=True):
        resource = ConfigResource("topic", topic_name)
        for k, v in config.items():
            resource.set_config(k, v, overwrite=overwrite)

        future = self._admin_client.alter_configs([resource])

        for res, f in future.items():
            return f.result()

    def delete(self, topic_names, timeout=30):
        future = self._admin_client.delete_topics(topic_names, operation_timeout=self._timeout)

        for topic, f in future.items():
            return f.result()
