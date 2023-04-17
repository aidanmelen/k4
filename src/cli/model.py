class BaseModel:
    def __init__(self):
        self._data = {}

    @property
    def data(self):
        raise NotImplemented


class TopicModel(BaseModel):
    @property
    def data(self):
        return {
            "name": "Topic",
            "info": {"context": None, "cluster": None, "user": None},
            "domains": {
                "1": "domain1",
                "2": "domain2",
                "3": "domain3",
                "4": "domain4",
                "5": "domain5",
                "6": "domain6",
                "7": "domain7",
                "8": "domain8",
                "9": "domain9",
                "10": "domain10",
            },
            "controls": {
                "c": "Consume",
                "ctrl-c": "Create",
                "ctrl-d": "Delete",
                "d": "Describe",
                "e": "Edit",
                "?": "Help",
                "i": "Show Internal",
            },
            "contents": [
                "TOPIC                              PARTITION",
                "_schemas_schemaregistry_confluent  1        ",
                "confluent.connect-configs          1        ",
                "confluent.connect-offsets          25       ",
                "confluent.connect-status           5        ",
            ],
        }


class ConsumerGroupModel(BaseModel):
    @property
    def data(self):
        return {
            "name": "ConsumerGroup",
            "info": {"context": None, "cluster": None, "user": None},
            "domains": {"1": "domain1", "2": "domain2", "3": "domain3"},
            "controls": {
                "ctrl-d": "Delete",
                "d": "Describe",
                "e": "Edit",
                "?": "Help",
                "i": "Show Internal",
            },
            "contents": [
                "GROUP                              TOPIC                                                                                          PARTITION    CURRENT-OFFSET    LOG-END-OFFSET    LAG    CONSUMER-ID                                                                                                                                 HOST        CLIENT-ID",
                "_confluent-controlcenter-7-3-0-0   _confluent-controlcenter-7-3-0-0-MetricsAggregateStore-repartition                             9            -                 20404             20404  _confluent-controlcenter-7-3-0-0-d74d63ac-128f-4564-8110-2ff76cf40c6b-StreamThread-7-consumer-c146c998-cb96-4ecb-98a5-785bf08d3938          /10.1.3.98  _confluent-controlcenter-7-3-0-0-d74d63ac-128f-4564-8110-2ff76cf40c6b-StreamThread-7-consumer",
                "_confluent-controlcenter-7-3-0-0   _confluent-controlcenter-7-3-0-0-MonitoringMessageAggregatorWindows-ONE_MINUTE-repartition     9            -                 0                 0      _confluent-controlcenter-7-3-0-0-d74d63ac-128f-4564-8110-2ff76cf40c6b-StreamThread-7-consumer-c146c998-cb96-4ecb-98a5-785bf08d3938          /10.1.3.98  _confluent-controlcenter-7-3-0-0-d74d63ac-128f-4564-8110-2ff76cf40c6b-StreamThread-7-consumer",
                "_confluent-controlcenter-7-3-0-0   _confluent-controlcenter-7-3-0-0-MonitoringMessageAggregatorWindows-THREE_HOURS-repartition    9            -                 0                 0      _confluent-controlcenter-7-3-0-0-d74d63ac-128f-4564-8110-2ff76cf40c6b-StreamThread-7-consumer-c146c998-cb96-4ecb-98a5-785bf08d3938          /10.1.3.98  _confluent-controlcenter-7-3-0-0-d74d63ac-128f-4564-8110-2ff76cf40c6b-StreamThread-7-consumer",
            ],
        }
