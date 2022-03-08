import mysql.connector


class Database:
    def __init__(self, host, user, password, database_name):
        self._conn = None
        try:
            self._conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database_name
            )
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        # If we don't use the commit() method after making any changes to the database,
        # the database will not be updated and changes will not be reflected.
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        try:
            self.cursor.execute(sql, params or ())
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))

    def fetchall(self):
        return self.cursor.fetchall()

    def query(self, sql, params=None):
        try:
            self.cursor.execute(sql, params or ())
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        return self.fetchall()
