from prometheus_client import Gauge, \
    Counter, Enum, \
    Summary, Histogram, Info


class Field(object):
    def __init__(
        self,
        name,
        column_type=str,
        default_value=str(),
        call="func",
        callback_func=lambda x: x
    ):
        self.name = name
        self.column_type = column_type
        self.callback_func = callback_func
        self.default_value = default_value
        self.call = call
        self.call_func = {
            "func": self.callback_func
        }

    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)


class EnumField(Enum):
    def __init__(
        self,
        name,
        documentation,
        states=[],
        call="state",
        default_value="",
        callback_func=lambda x: x
    ):
        super(EnumField, self).__init__(
            name,
            documentation,
            states=states
        )
        self.call_func = {
            "clear": self.clear,
            "collect": self.collect,
            "describe": self.describe,
            "labels": self.labels,
            "remove": self.remove,
            "state": self.state
        }
        self.name = name
        self.call = call
        self.default_value = default_value
        self.callback_func = callback_func


class SummaryField(Summary):
    def __init__(
        self,
        name,
        documentation,
        call="observe",
        default_value=0,
        callback_func=lambda x: x
    ):
        super(SummaryField, self).__init__(
            name,
            documentation,
        )
        self.call_func = {
            "clear": self.clear,
            "collect": self.collect,
            "describe": self.describe,
            "labels": self.labels,
            "observe": self.observe,
            "remove": self.remove,
            "time": self.time
        }
        self.name = name
        self.call = call
        self.default_value = default_value
        self.callback_func = callback_func


class HistogramField(Histogram):
    def __init__(
        self,
        name,
        documentation,
        call="observe",
        default_value=0,
        callback_func=lambda x: x
    ):
        super(HistogramField, self).__init__(
            name,
            documentation,
        )
        self.call_func = {
            "clear": self.clear,
            "collect": self.collect,
            "describe": self.describe,
            "labels": self.labels,
            "observe": self.observe,
            "remove": self.remove,
            "time": self.time
        }
        self.name = name
        self.call = call
        self.default_value = default_value
        self.callback_func = callback_func


class GaugeField(Gauge):

    def __init__(
        self,
        name,
        documentation,
        call="set",
        default_value=0,
        metric_labels=[],
        callback_func=lambda x: x
    ):
        super(GaugeField, self).__init__(
            name,
            documentation,
            metric_labels,
        )
        self.call_func = {
            "set": self.set,
            "inc": self.inc,
            "dec": self.dec,
            "clear": self.clear,
            "collect": self.collect,
            "describe": self.describe,
            "labels": self.labels,
            "remove": self.remove,
            "set_function": self.set_function,
            "set_to_current_time": self.set_to_current_time,
            "time": self.time,
            "track_inprogress": self.track_inprogress
        }
        self.name = name
        if metric_labels:
            self.labels(**metric_labels)
        self.call = call
        self.default_value = default_value
        self.callback_func = callback_func


class InfoField(Info):

    def __init__(
        self,
        name,
        documentation,
        call="info",
        default_value={},
        callback_func=lambda x: {"Info": x} if x else {"Info": "None"}
    ):
        super(InfoField, self).__init__(
            name,
            documentation,
        )
        self.call_func = {
            "clear": self.clear,
            "collect": self.collect,
            "describe": self.describe,
            "info": self.info,
            "labels": self.labels,
            "remove": self.remove
        }
        self.name = name
        self.call = call
        self.default_value = default_value
        self.callback_func = callback_func


class CounterField(Counter):

    def __init__(
        self,
        name,
        documentation,
        call="inc",
        default_value=0,
        callback_func=lambda x: x
    ):
        super(CounterField, self).__init__(
            name,
            documentation,
        )
        self.call_func = {
            "clear": self.clear,
            "collect": self.collect,
            "count_exceptions": self.count_exceptions,
            "describe": self.describe,
            "inc": self.inc,
            "labels": self.labels,
            "remove": self.remove
        }
        self.name = name
        self.call = call
        self.default_value = default_value
        self.callback_func = callback_func
