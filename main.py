from datetime import datetime
from database.database import Database


with Database('localhost', 'root', '778899', 'greenhouse') as db:
    sql = "insert into temperature (temperature, time) values (%s, %s)"
    value = (26.3, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), )
    db.execute(sql, value)
    comments = db.query('select * from temperature')
    print(comments)
