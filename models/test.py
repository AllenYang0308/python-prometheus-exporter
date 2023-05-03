def run():
    data = [
        {
            "id": "M123456",
            "model": "MODEL123456"
        },
        {
            "id": "M2222",
            "model": "MODEL2222"
        }
    ]
    mlist = [
        {
            "metric": "test",
            "labels": [x['id']],
            "kwargs": x
        } for x in data
    ]

    return mlist
