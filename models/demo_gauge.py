def run():

    data = [
        {
            "id": "ID00001",
            "name": "TEST00001",
            "model": "M00001",
            "value": 827348
        },
        {
            "id": "ID00002",
            "name": "TEST00002",
            "model": "M00002",
            "value": 7812634
        }
    ]

    rsp = [
        {
            "metric": "demo_gauge",
            "labels": [x['id'], x['name'], x['model']],
            "kwargs": {
                "gauge": x['value']
            }
        } for x in data
    ]

    return rsp
