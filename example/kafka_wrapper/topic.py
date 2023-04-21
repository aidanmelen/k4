from kafka_wrapper.topic import Topic
from cli import editor
import json


admin_client_config = {"bootstrap.servers": "localhost:9092"}

topic = Topic(admin_client_config, timeout=3)

print("List all Topics")
topic_list = topic.list()
print(json.dumps(topic_list, indent=4), "\n\n")

print("Create Topic")
topic_name = "test.topic"
if not topic.does_exist(topic_name):
    print(json.dumps(topic.create(topic_name, num_partitions=3, replication_factor=3, config={"cleanup.policy": "compact"}), indent=4), "\n\n")

print("List describe all Topics")
print(json.dumps(topic.describe(), indent=4), "\n\n")

print("Describe Topic")
print(json.dumps(topic.describe(topic_names=[topic_name]), indent=4), "\n\n")

print("Describe Topic config")
topic_configs = topic.describe_configs(topic_names=[topic_name])
print(json.dumps(topic_configs, indent=4, sort_keys=True), "\n\n")

print("Alter Topic")
topic_config = {k:v for k,v in topic_configs[topic_name].items() if v != "-"}
new_config = editor.open_config(topic_config)
print(json.dumps(topic.alter(topic_name, config=new_config), indent=4, sort_keys=True), "\n\n")

# print("And verify topic config alteration")
# topic_config = topic.describe_configs(topic_names=[topic_name])
# print(json.dumps(topic_config, indent=4, sort_keys=True), "\n\n")

print("Delete Topic")
if topic.does_exist(topic_name):
    print(json.dumps(topic.delete([topic_name]), indent=4), "\n\n")

