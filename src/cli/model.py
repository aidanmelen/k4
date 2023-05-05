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

    async def refresh(self, wait_seconds: int = 0) -> None:
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
        self.contents = self.client.list(show_internal=self.input.get("show_internal"))

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
            only_stable=self.input.get("show_stable"),
            only_high_level=self.input.get("show_high_level")
        )
        group_ids = [group["id"] for group in groups]
        top_namespaces = ["all"] + list(helper.get_top_prefixes(group_ids).keys())
        self.namespaces = dict(enumerate(top_namespaces))

    def update_controls(self) -> None:
        self.controls.update({
            "r": "Reset",
            "s": "Show Stable",
            "h": "Show High-Level",
        })

    def refresh_contents(self) -> None:
        group_ids = [
            g["id"] for g in self.client.list(
                only_stable=not self.input.get("show_stable"),
                only_high_level=not self.input.get("show_high_level")
            )
        ]
        self.contents = self.client.describe(group_ids=group_ids)
