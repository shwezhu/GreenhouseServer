import logging

from database.database_connection import DatabaseConnection
from http_server.http_server import HTTPServer
from mqtt_client import MQTTClient

logging.basicConfig(
    filename='system.log',
    filemode='a',
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding='utf-8',
    level=logging.INFO
)

db = DatabaseConnection('localhost', 'root', '778899', 'greenhouse')

mqtt_client = MQTTClient(db)

server = HTTPServer(
    '0.0.0.0',
    8080,
    db
)

mqtt_client.start_monitor()

while True:
    # select() returns a list of (key, events) tuples, one for each ready file object.
    # key is the SelectorKey instance corresponding to a ready file object.
    # events is a bitmask of events ready on this file object.
    # A SelectorKey is a namedtuple used to associate a file object to its
    # underlying file descriptor, selected event mask and attached data.
    # You can register multiple events for a socket.
    # The reported mask will tell you which of those events is actually ready.
    events = server.sel.select()
    for key, event_mask in events:
        callback = key.data
        callback(key.fileobj, event_mask)

# from datetime import datetime
# from database.database_connection import DatabaseConnection
# from database.database_utils import DatabaseUtils
# db = DatabaseUtils(DatabaseConnection('localhost', 'root', '778899', 'greenhouse'))
# sql = "insert into temperature (temperature, time) values (%s, %s)"
# value = (28.3, datetime.now().strftime('%Y-%m-%d %H:%M'))
# db.execute(sql, value)
# r = db.query('select * from temperature')
# print(r)
