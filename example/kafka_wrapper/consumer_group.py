from kafka_wrapper.consumer_group import ConsumerGroup
from tabulate import tabulate
import json
import os


admin_client_config = {"bootstrap.servers": os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")}

consumer_group = ConsumerGroup(admin_client_config, timeout=5)

print("List all Consumer Groups")
print(json.dumps(consumer_group.list(), indent=4), "\n\n")

# headers = [
#     "GROUP",
#     "TOPIC",
#     "PARTITION",
#     "CURRENT-OFFSET",
#     "LOG-END-OFFSET",
#     "LAG",
#     "CONSUMER-ID",
#     "HOST",
#     "CLIENT-ID",
# ]
# group_rows = []
# for group, metadata in consumer_group.describe(show_empty=True, show_simple=True).items():
#     for m in metadata.get("members", []):
#         assignments = m.get("assignments", [])

#         if assignments:
#             for a in assignments:
#                 group_rows.append(
#                     [
#                         group,
#                         a["topic"],
#                         a["partition"],
#                         a["current_offset"],
#                         a["log_end_offset"],
#                         a["lag"],
#                         m["id"],
#                         m["host"],
#                         m["client_id"],
#                     ]
#                 )
#         else:
#             group_rows.append([group,None,None,None,None,None,m["id"],m["host"],m["client_id"]])

# print("Tabulate List Consumer Groups")
# print(tabulate(group_rows, headers=headers, tablefmt="plain", numalign="left", maxcolwidths=[None, None, None, None, None, None, 20, 20, 20]))

print("List SIMPLE and EMPTY Consumer Groups")
all_groups = consumer_group.list(show_empty=True, show_simple=True)
print(json.dumps(all_groups, indent=4), "\n\n")

# print("Describe all Consumer Groups")
# print(json.dumps(consumer_group.describe(), indent=4), "\n\n")

# print("Describe all Consumer Groups without including offset lag")
# print(json.dumps(consumer_group.describe(include_offset_lag=False), indent=4), "\n\n")

# print("Describe one or many Consumer Groups")
# print(json.dumps(consumer_group.describe(group_ids=["_confluent-controlcenter-7-3-0-0-command"]), indent=4), "\n\n")

# print("Set admin_client and timeout")
# from confluent_kafka.admin import AdminClient
# consumer_group.admin_client = AdminClient({"bootstrap.servers": "kafka:9092", "socket.timeout.ms": 10})
# consumer_group.timeout = 3