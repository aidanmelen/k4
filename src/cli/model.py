from typing import List, Dict
from tabulate import tabulate
from kafka_wrapper.topic import Topic
from kafka_wrapper.consumer_group import ConsumerGroup

import time

class Timer:
    def __init__(self):
        self.__current_time = time.perf_counter()
        self.__last_time = self.__current_time
        self.__elapsed_time = 0

    @property
    def elapse_time(self):
        return self.__elapsed_time

    def has_time_elapsed(self, time_seconds: int):
        return self.__elapsed_time > time_seconds
    
    def lap(self):
        self.__current_time = time.perf_counter()
        self.__elapsed_time = self.__current_time - self.__last_time


class TopicModel:
    def __init__(self, admin_client_config: Dict[str, str], timeout: int = 10, refresh_wait_seconds: int = 10):
        self.client = Topic(admin_client_config=admin_client_config, timeout=timeout)
        self.timer = Timer()

        # Data Refresh
        self.__refresh_wait_seconds = refresh_wait_seconds

        # Data
        self.__name = "Topic"
        self.__info = {
            "context": None,
            "cluster": None,
            "user": None
        }
        self.__namespaces = {}
        self.__controls = {
            "c": "Consume",
            "ctrl-c": "Create",
            "ctrl-d": "Delete",
            "d": "Describe",
            "e": "Edit",
            "?": "Help",
            "i": "Show Internal",
            "p": "Produce",
        }
        self.__contents = []

    @property
    def refresh_wait_seconds(self):
        return self.__refresh_wait_seconds

    @refresh_wait_seconds.setter
    def refresh_wait_seconds(self, value: int):
        self.__refresh_wait_seconds = int(value)

    @property
    def name(self):
        return self.__name

    @property
    def info(self):
        return self.__info
    
    @property
    def namespaces(self):
        return self.__namespaces
    
    @property
    def contents(self):
        return self.__contents
    
    @property
    def controls(self):
        return self.__controls

    def get_top_namespaces(names: List[str] = [], max_value: int = 10):
        namespaces_counts = {}

        for string in lst:
            if string.startswith(("-", ".", "_")):
                namespaces = string.split(string[0], 1)[1].split(("-", ".", "_"), 1)[0]
            else:
                namespaces = string.split(("-", ".", "_"), 1)[0]

            if namespaces in namespaces_counts:
                namespaces_counts[namespaces] += 1
            else:
                namespaces_counts[namespaces] = 1

        sorted_namespaces_counts = sorted(namespaces_counts.items(), key=get_count, reverse=True)[:10]
        top_namespaces = {}
        for i, (namespaces, count) in enumerate(sorted_namespaces_counts):
            if i > max_value:
                # Only return top max namespaces
                break
            top_namespaces[str(i+1)] = namespaces

        return top_namespaces

    def refresh(self, refresh_wait_seconds: int = 10, **kwargs):    
        self.timer.lap()   
        if timer.has_time_elapsed(seconds=refresh_wait_seconds):

            # Refresh namespace data
            topics = self.client.list(**kwargs)
            topic_names = [topic["name"] for topic in topics]
            self.__namespaces = self.get_top_namespaces(topic_names)
            
            # Refresh contents data
            topics = self.client.list(**kwargs)
            headers = ["TOPIC", "PARTITION"]
            lines = [[r["name"], r["partitions"]] for r in topics]
            self.__contents = tabulate(lines, headers=headers, tablefmt="plain", numalign="left")


# class ConsumerGroupModel:
#     def __init__(self, admin_client_config, only_stable=True, only_high_level=True, timeout=10):
#         self.client = ConsumerGroup(admin_client_config, timeout=timeout)
#         self.only_stable = only_stable
#         self.only_high_level = only_high_level

#     def tabulate(self):
#         tabulated_data = [
#             # fmt: off
#             {"text": "GROUP                              TOPIC                                                                                          PARTITION    CURRENT-OFFSET    LOG-END-OFFSET    LAG    CONSUMER-ID                                                                                                                                 HOST        CLIENT-ID"},
#             {"text": "_confluent-controlcenter-7-3-0-0   _confluent-controlcenter-7-3-0-0-MetricsAggregateStore-repartition                             9            -                 20404             20404  _confluent-controlcenter-7-3-0-0-d74d63ac-128f-4564-8110-2ff76cf40c6b-StreamThread-7-consumer-c146c998-cb96-4ecb-98a5-785bf08d3938          /10.1.3.98  _confluent-controlcenter-7-3-0-0-d74d63ac-128f-4564-8110-2ff76cf40c6b-StreamThread-7-consumer"},
#             {"text": "_confluent-controlcenter-7-3-0-0   _confluent-controlcenter-7-3-0-0-MonitoringMessageAggregatorWindows-ONE_MINUTE-repartition     9            -                 0                 0      _confluent-controlcenter-7-3-0-0-d74d63ac-128f-4564-8110-2ff76cf40c6b-StreamThread-7-consumer-c146c998-cb96-4ecb-98a5-785bf08d3938          /10.1.3.98  _confluent-controlcenter-7-3-0-0-d74d63ac-128f-4564-8110-2ff76cf40c6b-StreamThread-7-consumer"},
#             {"text": "_confluent-controlcenter-7-3-0-0   _confluent-controlcenter-7-3-0-0-MonitoringMessageAggregatorWindows-THREE_HOURS-repartition    9            -                 0                 0      _confluent-controlcenter-7-3-0-0-d74d63ac-128f-4564-8110-2ff76cf40c6b-StreamThread-7-consumer-c146c998-cb96-4ecb-98a5-785bf08d3938          /10.1.3.98  _confluent-controlcenter-7-3-0-0-d74d63ac-128f-4564-8110-2ff76cf40c6b-StreamThread-7-consumer"},
#         ]
#         return tabulated_data

#     @property
#     def data(self):
#         return {
#             "name": "ConsumerGroup",
#             "info": {"context": None, "cluster": None, "user": None},
#             "namespaces": {"1": "domain1", "2": "domain2", "3": "domain3"},
#             "controls": {
#                 "ctrl-d": "Delete",
#                 "d": "Describe",
#                 "e": "Edit",
#                 "?": "Help",
#                 "i": "Show Internal",
#             },
#             "contents": self.tabulate()
#         }
