from kafka_wrapper.consumer_group import ConsumerGroup
from tabulate import tabulate
import json


admin_client_config = {"bootstrap.servers": "kafka:9092"}

consumer_group = ConsumerGroup(admin_client_config, timeout=5)

print("List all Consumer Groups")
print(json.dumps(consumer_group.list(), indent=4), "\n\n")

headers = [
    "GROUP",
    "TOPIC",
    "PARTITION",
    "CURRENT-OFFSET",
    "LOG-END-OFFSET",
    "LAG",
    "CONSUMER-ID",
    "HOST",
    "CLIENT-ID",
]
group_rows = []
for group, metadata in consumer_group.describe().items():
    for m in metadata.get("members", []):
        for a in m.get("assignments", []):
            group_rows.append(
                [
                    group,
                    a["topic"],
                    a["partition"],
                    a["current_offset"],
                    a["log_end_offset"],
                    a["lag"],
                    m["id"],
                    m["host"],
                    m["client_id"],
                ]
            )

print("Tabulate List all Consumer Groups")
print(tabulate(group_rows, headers=headers, tablefmt="plain", numalign="left"))

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