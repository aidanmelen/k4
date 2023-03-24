from kafka_wrapper.broker import Broker
from k4.helpers import open_editor
import json


broker = Broker({"bootstrap.servers": "kafka:9092"}, timeout=3)

print("List all Brokers")
print(json.dumps(broker.list(), indent=4), "\n\n")

print("Describe all Brokers")
print(json.dumps(broker.describe(), indent=4), "\n\n")

print("Describe Broker controller configs")
broker_configs = broker.describe_configs()
print(broker_configs)
print(json.dumps(broker.describe_configs(), indent=4, sort_keys=True), "\n\n")

print("Alter all Brokers")
per_topic_configs = broker.describe_configs(dynamic_only=True)
new_per_topic_configs = open_editor(per_topic_configs)
print(json.dumps(broker.alter(config=new_per_topic_configs), indent=4, sort_keys=True), "\n\n")

# print("And verify broker config alteration")
# broker_config = broker.describe_configs(broker_ids=['2'])
# print(json.dumps(broker_config, indent=4, sort_keys=True), "\n\n")