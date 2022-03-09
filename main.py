from datetime import datetime
from database.database_connection import DatabaseConnection
from database.database_utils import DatabaseUtils

db = DatabaseUtils(DatabaseConnection('localhost', 'root', '778899', 'greenhouse'))
sql = "insert into temperature (temperature, time) values (%s, %s)"
value = (28.3, datetime.now().strftime('%Y-%m-%d %H:%M'))
db.execute(sql, value)
r = db.query('select * from temperature')
print(r)
