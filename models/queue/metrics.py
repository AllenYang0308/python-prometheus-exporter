from prometheus_client import Gauge, Info
from models.base.models import Model
from models.base.fields import Field


class Demo(Model):
    name = Field("name", callback_func=lambda x: str(x))
    model = Field("model", callback_func=lambda x: str(x))


class Test(Model):
    model = Field("model", callback_func=lambda x: str(x))


class DemoGauge(Model):
    gauge = Field("gauge", callback_func=lambda x: float(x))


# -------------------- Metric Model --------------------
class MetricDataModel(object):
    Demo = Demo
    DemoGauge = DemoGauge
    Test = Test


class Metrics(object):
    demo = Info(
        "demo",
        "demo",
        ["id"]
    )
    demo_gauge = Gauge(
        "demo_gauge",
        "demo",
        ['id', 'name', 'model']
    )
    test = Info(
        "test",
        "test",
        ["id"]
    )
