import mysql.connector


class DatabaseUtils:
    @staticmethod
    def connect_sql():
        print("Connecting database...")
        try:
            db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="778899",
                database="greenhouse"
            )
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return None  # Don't know None? See syntax.md
        print("Database connected")
        return db_connection

    @staticmethod
    def insert(connection, sql, value):
        cursor = connection.cursor()
        try:
            cursor.execute(sql, value)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return None
        # If we don't use the commit() method after making any changes to the database,
        # the database will not be updated and changes will not be reflected.
        connection.commit()

    @staticmethod
    def select(connection, sql):
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        result = cursor.fetchall()
        return result
