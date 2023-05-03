from models.base.fields import Field
from models.base.models import Model
from models.queue.metrics import Metrics


class ApiCurrMdsStatus(Model):

    mds_id = Field("mds_id")
    Key_Name = Field("Key_Name")
    ID = Field("ID")
    value = Field("value")
    Unit = Field("Unit")


class MetricsInfo(object):

    def __init__(self, metric="", labels=[], kwargs=dict()):
        self.metric = getattr(Metrics, metric) \
            if hasattr(Metrics, metric) else None
        self.labels = labels
        self.data = kwargs

    def set_metric_info(self):
        if self.metric and self.labels[0] != " ":
            self.metric.labels(*self.labels).info(self.data)
        else:
            pass


class MetricsGauge(object):

    def __init__(self, metric="", labels=[], kwargs=dict()):
        self.metric = getattr(Metrics, metric) \
            if hasattr(Metrics, metric) else None
        self.labels = labels
        self.data = kwargs

    def set_metric_info(self):
        if self.metric and self.labels[0] != " ":
            self.metric.labels(*self.labels).set(self.data['gauge'])
        else:
            pass
