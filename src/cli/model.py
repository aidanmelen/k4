from typing import List, Dict, Any
from tabulate import tabulate
from kafka_wrapper.topic import Topic
from kafka_wrapper.consumer_group import ConsumerGroup
from .timer import Timer
from . import helper

import re

class TopicModel:
    def __init__(self, admin_client_config: Dict[str, str], timeout: int = 10) -> None:
        self.client = Topic(admin_client_config=admin_client_config, timeout=timeout)
        self.timer = Timer()

        # Data
        self.__name = "Topic"
        self.__info = {"context": None, "cluster": None, "user": None}
        self.__namespaces = {}
        self.__controls = {
            "c": "Consume",
            "shift-c": "Create",
            "ctrl-d": "Delete",
            "d": "Describe",
            "e": "Edit",
            "?": "Help",
            "i": "Show Internal",
            "p": "Produce",
        }
        self.__contents = []

    @property
    def name(self) -> str:
        return self.__name

    @property
    def info(self) -> Dict[str, str]:
        return self.__info

    @property
    def namespaces(self) -> Dict[str, str]:
        return self.__namespaces

    @property
    def contents(self) -> List[str]:
        return self.__contents

    @property
    def controls(self) -> Dict[str, str]:
        return self.__controls

    def refresh_namespaces(self) -> None:
        topics = self.client.list()
        topic_names = [topic["name"] for topic in topics]
        top_namespaces = list(helper.get_top_prefixes(topic_names).keys())
        self.__namespaces = dict(enumerate(top_namespaces))

    def refresh_contents(self) -> None:
        topics = self.client.list()
        headers = ["TOPIC", "PARTITION"]
        lines = [[r["name"], r["partitions"]] for r in topics]
        self.__contents = tabulate(lines, headers=headers, tablefmt="plain", numalign="left").splitlines()

        # self.__contents = [
        #     "TOPIC                              PARTITION",
        #     "_schemas_schemaregistry_confluent  1        ",
        #     "confluent.connect-configs          1        ",
        #     "confluent.connect-offsets          25       ",
        #     "confluent.connect-status           5        ",
        # ]

    def refresh(self, wait_seconds: int = 10) -> None:
        if self.timer.has_elapsed(seconds = wait_seconds):
            self.refresh_namespaces()
            self.refresh_contents()
            self.timer.reset()


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
