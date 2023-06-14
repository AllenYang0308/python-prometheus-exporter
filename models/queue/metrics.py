from prometheus_client import Gauge, Info
from models.base.models import Model
from models.base.fields import Field


class ServiceStatusModel(Model):
    gauge = Field("gauge", callback_func=lambda x: float(x))


class Demo(Model):
    name = Field("name", callback_func=lambda x: str(x))
    model = Field("model", callback_func=lambda x: str(x))


# -------------------- Metric Model --------------------
class MetricDataModel(object):
    Demo = Demo
    ServiceStatusModel = ServiceStatusModel


class Metrics(object):
    demo = Info(
        "demo",
        "demo",
        ["id"]
    )
    service_status_gauge = Gauge(
        "service_status_gauge",
        "demo",
        ["target_name", "target_url", "status"]
    )
