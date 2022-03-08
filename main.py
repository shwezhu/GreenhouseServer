from datetime import datetime
from database_utils import DatabaseUtils


connection = DatabaseUtils.connect_sql()
now = datetime.now()
temperature = 23.7
date = now.strftime('%Y-%m-%d %H:%M:%S')
sql = "insert into temperature (temperature, time) values (%s, %s)"
value = (temperature, date)
DatabaseUtils.insert(connection, sql, value)

# sql = "select * from  temperature"
# result = DatabaseUtils.select(connection, sql)
# for r in result:
#     print(r)

connection.close()
