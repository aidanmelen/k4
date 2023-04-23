from typing import List, Dict, Any
from tabulate import tabulate
from kafka_wrapper.topic import Topic
from kafka_wrapper.consumer_group import ConsumerGroup
from .timer import Timer
from . import helper

import re
import os

class BaseModel:
    def __init__(self, admin_client_config: Dict[str, str], timeout: int = 10) -> None:
        self.name = None
        self.bootstrap_servers = admin_client_config.get("bootstrap.servers")
        self.info = {"context": None, "cluster": self.bootstrap_servers, "user": None}
        self.namespaces = {}
        self.controls = {}
        self.contents = []
        self.client = None
        self.timer = Timer()

    def refresh_info(self) -> None:
        self.info = {"context": None, "cluster": self.bootstrap_servers, "user": None}

    def refresh_namespaces(self) -> None:
        self.namespace = {}

    def refresh_controls(self) -> None:
        self.controls = {}

    def refresh_contents(self) -> None:
        self.contents = []

    def refresh(self, wait_seconds: int = 10) -> None:
        if self.timer.has_elapsed(seconds = wait_seconds):
            self.refresh_info()
            self.refresh_namespaces()
            self.refresh_controls()
            self.refresh_contents()
            self.timer.reset()

class TopicModel(BaseModel):
    def __init__(self, admin_client_config: Dict[str, str], timeout: int = 10) -> None:
        super().__init__(admin_client_config, timeout=timeout)
        
        self.name = "Topic"
        
        if not os.environ.get("K4_DEBUG_OFFLINE"):
            self.client = Topic(admin_client_config=admin_client_config, timeout=timeout)
        else:
            self.client = None

    def refresh_info(self) -> None:
        self.info = {"context": None, "cluster": self.bootstrap_servers, "user": None}

    def refresh_namespaces(self) -> None:
        if not os.environ.get("K4_DEBUG_OFFLINE"):
            topics = self.client.list()
            topic_names = [topic["name"] for topic in topics]
            top_namespaces = list(helper.get_top_prefixes(topic_names).keys())
            self.namespaces = dict(enumerate(top_namespaces))
        else:
            self.namespaces = {
                0: "confluent",
                1: "schemas",
            }

    def refresh_controls(self) -> None:
        self.controls = {
            "c": "Consume",
            "shift-c": "Create",
            "ctrl-d": "Delete",
            "d": "Describe",
            "e": "Edit",
            "?": "Help",
            "i": "Show Internal",
            "p": "Produce",
        }

    def refresh_contents(self) -> None:
        if os.environ.get("K4_DEBUG_OFFLINE"):
            self.contents = [
                "TOPIC                              PARTITION",
                "_schemas_schemaregistry_confluent  1        ",
                "confluent.connect-configs          1        ",
                "confluent.connect-offsets          25       ",
                "confluent.connect-status           5        ",
            ]
        else:
            topics = self.client.list()
            headers = ["TOPIC", "PARTITION"]
            lines = [[r["name"], r["partitions"]] for r in topics]
            self.contents = tabulate(lines, headers=headers, tablefmt="plain", numalign="left").splitlines()


class ConsumerGroupModel(BaseModel):
    def __init__(self, admin_client_config: Dict[str, str], timeout: int = 10) -> None:
        super().__init__(admin_client_config, timeout=timeout)
        
        self.name = "ConsumerGroup"
        
        if not os.environ.get("K4_DEBUG_OFFLINE"):
            self.client = ConsumerGroup(admin_client_config=admin_client_config, timeout=timeout)
        else:
            self.client = None

    def refresh_info(self) -> None:
        self.info = {"context": None, "cluster": self.bootstrap_servers, "user": None}

    def refresh_namespaces(self) -> None:
        if not os.environ.get("K4_DEBUG_OFFLINE"):
            groups = self.client.list(only_stable=True, only_high_level=True)
            group_ids = [group["id"] for group in groups]
            top_namespaces = list(helper.get_top_prefixes(group_ids).keys())
            self.namespaces = dict(enumerate(top_namespaces))
        else:
            self.namespaces = {
                0: "confluent",
            }

    def refresh_controls(self) -> None:
        self.controls = {
            "ctrl-d": "Delete",
            "d": "Describe",
            "e": "Edit",
            "?": "Help",
            "r": "Reset",
        }

    def refresh_contents(self) -> None:
        if os.environ.get("K4_DEBUG_OFFLINE"):
            self.contents = [
                "GROUP                              TOPIC                                                                                          PARTITION    CURRENT-OFFSET    LOG-END-OFFSET    LAG    CONSUMER-ID                                                                                                                                 HOST        CLIENT-ID",
                "_confluent-controlcenter-7-3-0-0   _confluent-controlcenter-7-3-0-0-MetricsAggregateStore-repartition                             9            -                 20404             20404  _confluent-controlcenter-7-3-0-0-d74d63ac-128f-4564-8110-2ff76cf40c6b-StreamThread-7-consumer-c146c998-cb96-4ecb-98a5-785bf08d3938          /10.1.3.98  _confluent-controlcenter-7-3-0-0-d74d63ac-128f-4564-8110-2ff76cf40c6b-StreamThread-7-consumer",
                "_confluent-controlcenter-7-3-0-0   _confluent-controlcenter-7-3-0-0-MonitoringMessageAggregatorWindows-ONE_MINUTE-repartition     9            -                 0                 0      _confluent-controlcenter-7-3-0-0-d74d63ac-128f-4564-8110-2ff76cf40c6b-StreamThread-7-consumer-c146c998-cb96-4ecb-98a5-785bf08d3938          /10.1.3.98  _confluent-controlcenter-7-3-0-0-d74d63ac-128f-4564-8110-2ff76cf40c6b-StreamThread-7-consumer",
                "_confluent-controlcenter-7-3-0-0   _confluent-controlcenter-7-3-0-0-MonitoringMessageAggregatorWindows-THREE_HOURS-repartition    9            -                 0                 0      _confluent-controlcenter-7-3-0-0-d74d63ac-128f-4564-8110-2ff76cf40c6b-StreamThread-7-consumer-c146c998-cb96-4ecb-98a5-785bf08d3938          /10.1.3.98  _confluent-controlcenter-7-3-0-0-d74d63ac-128f-4564-8110-2ff76cf40c6b-StreamThread-7-consumer",
            ]
        else:
            headers = [
                "GROUP",
                "TOPIC",
                "PARTITION",
                "CURRENT-OFFSET",
                "LOG-END-OFFSET",
                "LAG",
                "STATUS"
                # "CONSUMER-ID",
                # "HOST",
                # "CLIENT-ID",
            ]
            lines = []
            for group, metadata in self.client.describe().items():
                for m in metadata.get("members", []):
                    for a in m.get("assignments", []):
                        lines.append(
                            [
                                group,
                                a["topic"],
                                a["partition"],
                                a["current_offset"],
                                a["log_end_offset"],
                                a["lag"],
                                "Running" if all([m["id"], m["host"], m["client_id"]]) else "Stopped"
                                # m["id"],
                                # m["host"],
                                # m["client_id"],
                            ]
                        )
            self.contents = tabulate(lines, headers=headers, tablefmt="plain", numalign="left").splitlines()
