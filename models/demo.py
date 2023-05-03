def run():
    data = [
        {
            "id": "M123456",
            "name": "TEST123456",
            "model": "MODEL123456"
        },
        {
            "id": "M2222",
            "name": "TEST2222",
            "model": "MODEL2222"
        }
    ]
    mlist = [
        {
            "metric": "demo",
            "labels": [x['id']],
            "kwargs": x
        } for x in data
    ]

    return mlist
