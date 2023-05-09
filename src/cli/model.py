from tabulate import tabulate
from typing import List, Dict, Any
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
        self.controls = {
            "shift-c": "Create",
            "d": "Describe",
            "e": "Edit",
            "ctrl-d": "Delete",
            "?": "Help",
        }
        self.contents = []
        self.client = None
        self.timer = Timer()
        self.input = {}

    def update_input(self, data: Dict[str, str]) -> None:
        self.input = data

    def refresh_info(self) -> None:
        self.info = {"context": None, "cluster": self.bootstrap_servers, "user": None}

    def refresh_namespaces(self) -> None:
        self.namespace = {}
    
    def get_sorted_controls(self):
        """Returns the controls dictionary sorted by value."""
        return dict(sorted(self.controls.items(), key=lambda x: x[1]))

    def refresh_contents(self) -> None:
        self.contents = []

    def refresh(self, wait_seconds: int = 0) -> None:
        if self.timer.has_elapsed(seconds = wait_seconds):
            self.refresh_info()
            self.refresh_namespaces()
            self.refresh_contents()
            self.timer.reset()

class TopicModel(BaseModel):
    def __init__(self, admin_client_config: Dict[str, str], timeout: int = 10) -> None:
        super().__init__(admin_client_config, timeout=timeout)
        
        self.name = "Topic"
        self.client = Topic(admin_client_config=admin_client_config, timeout=timeout)
        self.update_controls()

    def refresh_namespaces(self) -> None:
        topics = self.client.list(show_internal=self.input.get("show_internal"))
        topic_names = [topic["name"] for topic in topics]
        top_namespaces = ["all"] + list(helper.get_top_prefixes(topic_names).keys())
        self.namespaces = dict(enumerate(top_namespaces))

    def update_controls(self) -> None:
        self.controls.update({
            "p": "Produce",
            "c": "Consume",
            "i": "Show Internal",
        })

    def refresh_contents(self) -> None:
        topics = self.client.list(show_internal=self.input.get("show_internal"))
        headers = ["TOPIC", "PARTITIONS"]
        lines = [[topic["name"], topic["partitions"]] for topic in topics]
        tabulated_lines = tabulate(lines, headers=headers, tablefmt="plain", numalign="left", stralign="left").splitlines()
        header = tabulated_lines[0]

        for k, ns in self.namespaces.items():
            if int(self.input["namespace"]) == 0:
                self.contents = [header] + sorted(tabulated_lines[1:])
            elif int(k) == int(self.input["namespace"]):
                self.contents = [header] + sorted([line for line in tabulated_lines if line.lower().startswith(ns) or line.lower().startswith(f"_{ns}") or line.lower().startswith(f"__{ns}")])

class ConsumerGroupModel(BaseModel):
    def __init__(self, admin_client_config: Dict[str, str], timeout: int = 10) -> None:
        super().__init__(admin_client_config, timeout=timeout)
        
        self.name = "ConsumerGroup"
        self.client = ConsumerGroup(admin_client_config=admin_client_config, timeout=timeout)
        self.update_controls()

    # def refresh_info(self) -> None:
    #     self.info = {"context": None, "cluster": self.bootstrap_servers, "user": None}

    def refresh_namespaces(self) -> None:
        groups = self.client.list(
            show_empty=self.input.get("show_empty"),
            show_simple=self.input.get("show_simple")
        )
        group_ids = [group["id"] for group in groups]
        top_namespaces = ["all"] + list(helper.get_top_prefixes(group_ids).keys())
        self.namespaces = dict(enumerate(top_namespaces))

    def update_controls(self) -> None:
        self.controls.update({
            "r": "Reset",
            "shift-e": "Show Empty",
            "s": "Show Simple",
        })

    def refresh_contents(self) -> None:
        groups = self.client.list(
            show_empty=self.input.get("show_empty"),
            show_simple=self.input.get("show_simple")
        )
        headers = ["ID", "TYPE", "STATE"]
        lines = [[g["id"], g["type"].upper(), g["state"]] for g in groups]
        tabulated_lines = tabulate(lines, headers=headers, tablefmt="plain", numalign="left", stralign="left").splitlines()
        header = tabulated_lines[0]

        for k, ns in self.namespaces.items():
            if int(self.input["namespace"]) == 0:
                self.contents = [header] + sorted(tabulated_lines[1:])
            elif int(k) == int(self.input["namespace"]):
                self.contents = [header] + sorted([line for line in tabulated_lines if line.lower().startswith(ns) or line.lower().startswith(f"_{ns}") or line.lower().startswith(f"__{ns}")])
