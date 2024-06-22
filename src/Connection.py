import mysql.connector, os

class Connection(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Connection, cls).__new__(cls)
            cls._instance.connect()
            
        return cls._instance

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=os.environ['DB_HOST'] or 'localhost',
                user=os.environ['DB_USERNAME'] or 'user',
                password=os.environ['DB_PASSWORD'] or 'pass',
                database=os.environ['DB_DATABASE'] or ''
            )
            return True
        except Exception as e:
            print("Ошибка подключения:", e)
            return False

    @property
    def connection(self):
        return self._connection

    @connection.setter
    def connection(self, value):
        self._connection = value

    def close(self):
        if self.connection is not None:
            self.connection.close()

    def query(self, sql_query, args = []):
        cursor = self.connection.cursor()
        result = cursor.execute(sql_query, args)
        return result

    def fetch_all(self, query, args = []):
        rows = []
        for row in self.query(query, args):
            rows.append(row)
        return rows
