from confluent_kafka.admin import ConfigResource, ConfigSource, ResourceType
from .kafka_resource import KafkaResource
from .consumer_group import ConsumerGroup


class Broker(KafkaResource):
    def __init__(self, admin_client_config, timeout=10, log_level=None):
        """
        The Kafka Broker wrapper class.
        Args:
            admin_client_config (dict): The Kafka AdminClient configuration.
            timeout (int): The timeout for kafka operations.
            log_level (str): The logging level to use for the logger and console handler. Defaults to "NOTSET".
        """
        super().__init__(
            admin_client_config=admin_client_config, timeout=timeout, log_level=log_level
        )

    def list(self):
        """
        List Kafka Brokers.
        """
        metadata = self._admin_client.list_topics(timeout=self._timeout)

        brokers = []
        for broker_id, broker_metadata in metadata.brokers.items():
            brokers.append(
                {
                    "name": broker_id,
                    "type": "controller" if broker_id == metadata.controller_id else "worker",
                    "endpoint": f"{broker_metadata.host}:{broker_metadata.port}",
                }
            )

        return brokers

    def create(self):
        """
        Create a Kafka Broker.
        """
        raise NotImplemented

    def describe(self, consumer_group=None):
        """
        Describe one or many Kafka Brokers.
        """
        metadata = self._admin_client.list_topics(timeout=self._timeout)

        results = {}
        topics = []
        partitions = []
        replicas = []
        groups = []

        for topic_name, topic in metadata.topics.items():
            topics.append(topic)

            for partition in topic.partitions.values():
                partitions.append(partition)

                for broker in partition.replicas:
                    replicas.append(replicas)

        if isinstance(consumer_group, ConsumerGroup):
            self._consumer_group = consumer_group
        else:
            self._consumer_group = ConsumerGroup(self._admin_client_config, timeout=self._timeout)

        groups = self._consumer_group.list(only_stable=True, only_high_level=True)

        results["brokers"] = len(metadata.brokers.values())
        results["topics"] = len(topics)
        results["partitions"] = len(partitions)
        results["replicas"] = len(replicas)
        results["consumer_groups"] = len(groups)

        return results

    def describe_configs(self, broker_id=None, dynamic_only=False):
        """
        Describe one Kafka Broker configurations.
        """
        metadata = self._admin_client.list_topics(timeout=self._timeout)

        if broker_id:
            resource = ConfigResource(ResourceType.BROKER, str(broker_id))
        else:
            resource = ConfigResource(ResourceType.BROKER, str(metadata.controller_id))


        # Only one ConfigResource of type BROKER is allowed per call
        future = self._admin_client.describe_configs([resource], request_timeout=self._timeout)

        results = {}
        for res, f in future.items():
            config_entries = f.result()

            for config_entry in config_entries.values():

                # https://docs.confluent.io/platform/current/kafka/dynamic-config.html
                if dynamic_only and (config_entry.is_read_only or not config_entry.value):
                    continue

                # https://docs.confluent.io/platform/current/kafka/dynamic-config.html#updating-ssl-trust-store-of-an-existing-listener
                if dynamic_only and (
                    config_entry.name in ["ssl.keystore.type", "ssl.truststore.type"]
                ):
                    continue

                results[config_entry.name] = config_entry.value

        return results

    def alter(self, config, broker_ids=[], overwrite=True):
        """
        Alter configuration for all brokers in the Kafka Cluster atomically, replacing non-specified configuration properties with the cluster default values.
        """
        metadata = self._admin_client.list_topics(timeout=self._timeout)

        if not broker_ids:
            resources = [ConfigResource(ResourceType.BROKER, str(broker_id)) for broker_id, md in metadata.brokers.items()]
        else:
            resources = [ConfigResource(ResourceType.BROKER, str(broker_id)) for broker_id in broker_ids]

        for resource in resources:
            for k, v in config.items():
                resource.set_config(k, v, overwrite=overwrite)

            # Only one ConfigResource of type BROKER is allowed per call
            future = self._admin_client.alter_configs([resource])

            for res, f in future.items():
                f.result()

    def delete(self):
        raise NotImplemented
