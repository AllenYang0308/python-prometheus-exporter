import asyncio
import requests
from requests.exceptions import ConnectionError
from requests.models import Response
import yaml


def get_url_status(name, url, payload=None):

    try:
        rsp = requests.get(url)
    except ConnectionError:
        rsp = Response()
        rsp.status_code = 404

    return {
        "target_name": name,
        "target_url": url,
        "status": str(rsp.status_code),
        "response_time": rsp.elapsed.total_seconds()
    }


async def Async_get(name, url, loop, payload=None):

    rsp = await loop.run_in_executor(None, get_url_status, name, url)
    return rsp


async def run_task(*tasks):
    loop = asyncio.get_event_loop()
    t = list()
    for task in tasks:
        t.append(
            loop.create_task(
                Async_get(
                    task["name"],
                    task["url"],
                    loop,
                    None
                )
            )
        )
    x = await asyncio.gather(*t)
    return x


# if __name__ == '__main__':
def run():

    yaml.warnings({'YAMLLoadWarning': False})
    with open("models/config/services.yaml") as f:
        tasks = yaml.load(f)

    task_list = tasks["tasks"]
    r = asyncio.run(run_task(*task_list))
    rsp = [
        {
            "metric": "service_status_gauge",
            "labels": [x['target_name'], x['target_url'], x['status']],
            "kwargs": {
                "gauge": x['response_time']
            }
        } for x in r
    ]

    return rsp
