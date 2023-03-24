from kafka_wrapper.consumer_group import ConsumerGroup
import json


consumer_group = ConsumerGroup({"bootstrap.servers": "kafka:9092"}, timeout=5)

print("List all Consumer Groups")
print(json.dumps(consumer_group.list(), indent=4), "\n\n")

print("List only STABLE and HIGH-LEVEL Consumer Groups")
print(json.dumps(consumer_group.list(only_stable=True, only_high_level=True), indent=4), "\n\n")

print("Describe all Consumer Groups")
print(json.dumps(consumer_group.describe(), indent=4), "\n\n")

print("Describe all Consumer Groups without including offset lag")
print(json.dumps(consumer_group.describe(include_offset_lag=False), indent=4), "\n\n")

print("Describe one or many Consumer Groups")
print(json.dumps(consumer_group.describe(group_ids=["_confluent-controlcenter-7-3-0-0-command"]), indent=4), "\n\n")

print("Set admin_client and timeout")
from confluent_kafka.admin import AdminClient
consumer_group.admin_client = AdminClient({"bootstrap.servers": "kafka:9092", "socket.timeout.ms": 10})
consumer_group.timeout = 3