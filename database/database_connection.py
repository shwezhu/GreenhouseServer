import sys

import mysql.connector
import logging

from http_server.http_server import HTTPServer


class DatabaseConnection:
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
            logging.fatal(str(err) + ' in DatabaseConnection.__init__ method')
            sys.exit()
        self._cursor = self._conn.cursor()

    def __del__(self):
        self._conn.close()

    def execute(self, sql, params=None, conn=None):
        try:
            self.cursor.execute(sql, params or ())
        # mysql.connector.errors.Error: DatabaseError, InterfaceError, PoolError
        # except (mysql.connector.InterfaceError, mysql.connector.Error) as err:
        except mysql.connector.errors.Error as err:
            logging.error(str(err) + ' in DatabaseConnection.execute method')
            if conn is not None:
                HTTPServer.handle_error(conn, '404 Not Found', str(err))
            return None
        self.commit()

    def query(self, conn, sql, params=None):
        try:
            self.cursor.execute(sql, params or ())
        except mysql.connector.errors.Error as err:
            logging.error(str(err) + ' in DatabaseConnection.query method')
            HTTPServer.handle_error(conn, '404 Not Found', str(err))
            return None
        return self.__fetchall()

    @property
    def __connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.__connection.commit()

    def close(self, commit=True):
        # If we don't use the commit() method after making any changes to the database,
        # the database will not be updated and changes will not be reflected.
        if commit:
            self.commit()
        self.__connection.close()

    def __fetchall(self):
        return self.cursor.fetchall()
