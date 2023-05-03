import yaml
from models.base.fields import Field
from models.base.models import Model
from prometheus_client import start_http_server
from models.queue.queue import SingletonQueue, PeriodicWorker
from dotenv import load_dotenv
import models


class PeriodicWorkerParam(Model):
    name = Field("name")
    model = Field("model")
    formatter = Field("formatter")
    metric = Field(
        "metric",
        default_value="Info",
        callback_func=lambda x: str(x)
    )


if __name__ == '__main__':
    load_dotenv()
    with open("settings.yaml") as f:
        config = yaml.load(f.read())

    start_http_server(8008)
    job_queue = SingletonQueue(queue_name="default").queue
    for conf in config['settings']:
        function = getattr(models, conf['model'])
        interval = conf['interval']
        kwargs = PeriodicWorkerParam(**conf).convert()
        PeriodicWorker(
            interval,
            function.run,
            **PeriodicWorkerParam(**conf).convert()
        ).start()
