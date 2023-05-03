import os
import time
from queue import Queue
import threading
import models
from models.queue.models import MetricsInfo, MetricsGauge
from models.queue.metrics import MetricDataModel
# from models.base.logger import SingletonLogger as init_logger


def runner(
    worker_name="TasksWorker",
    queue_name="default",
    thread_num=1,
    queue=None,
    metric="Info"
):
    workerlist = {
        'TasksWorker': TasksWorker,
        'JobsWorker': JobsWorker
    }
    tasks = list()
    for x in range(thread_num):

        task = workerlist[worker_name](
            queue=SingletonQueue(queue_name).queue,
            thread_num=x,
            metric=metric
        )
        tasks.append(task)
        task.start()

    for t in tasks:
        t.join()


def SingletonMeta(cls):

    instances = {}

    def _singleton(queue_name="default", *args, **kwargs):
        if queue_name not in instances:
            instances[queue_name] = cls(*args, **kwargs)
        return instances[queue_name]
    return _singleton


@SingletonMeta
class SingletonQueue(object):

    def __init__(self, queue_name="default", *args, **kwargs):
        self.queue = Queue()


class TasksWorker(threading.Thread):

    Metric = {
        "Info": MetricsInfo,
        "Gauge": MetricsGauge
    }

    def __init__(self, queue, thread_num, metric="Info"):

        threading.Thread.__init__(self)
        self.queue = queue
        self.thread_num = thread_num
        self.metric_model = self.Metric[metric]

    def run(self):
        while self.queue.qsize() > 0:
            data = self.queue.get()
            # MetricsInfo(**data).set_metric_info()
            self.metric_model(**data).set_metric_info()


class JobsWorker(threading.Thread):

    def __init__(self, queue, thread_num, metric="Info"):

        threading.Thread.__init__(self)
        self.queue = queue
        self.thread_num = thread_num

    def run(self):

        while self.queue.qsize() > 0:
            data = self.queue.get()
            self.queue.put(data)
            try:
                formatter = getattr(MetricDataModel, data['formatter'])
                tasks = getattr(models, data['model']).run()
                # thread_num = int(len(tasks) / 3) if len(tasks) > 3 else 1
                thread_num = 15
                task_queue = SingletonQueue(queue_name=data['model']).queue
                for task in tasks:
                    task['kwargs'] = formatter(**task['kwargs']).convert()
                    task_queue.put(task)
                runner(
                    worker_name="TasksWorker",
                    queue_name=data['model'],
                    thread_num=thread_num,
                    queue=task_queue
                )

                time.sleep(data['interval'])
            except Exception:
                pass


class PeriodicWorker(threading.Timer):

    def __init__(self, interval, function, *args, **kwargs):
        threading.Timer.__init__(self, interval, function)
        self.args = args
        self.kwargs = kwargs
        # self.logger = init_logger(filename=os.getenv("log_file")).logger

    def run(self):
        while not self.finished.wait(self.interval):
            try:
                formatter = getattr(MetricDataModel, self.kwargs['formatter'])
                tasks = self.function()
                # thread_num = int(len(tasks)/3) if len(tasks) > 3 else 1
                thread_num = 3
                task_queue = SingletonQueue(
                    queue_name=self.kwargs['model']
                ).queue
                for task in tasks:
                    task['kwargs'] = formatter(**task['kwargs']).convert()
                    task_queue.put(task)
                    runner(
                        worker_name="TasksWorker",
                        queue_name=self.kwargs['model'],
                        thread_num=thread_num,
                        queue=task_queue,
                        metric=self.kwargs['metric']
                    )
            except Exception as e:
                self.logger.fatal(e)
