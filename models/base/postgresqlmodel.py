import psycopg2


class MigoPostgreSQL(object):

    def __init__(
        self,
        host="",
        database="",
        user="",
        password=""
    ):
        self._connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )

    @property
    def connection(self):
        return self._connection

    @connection.deleter
    def connection(self):
        self._connection.close()
        del self._connection
