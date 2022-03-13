import sys
import socket
import selectors
import json

from database.database_connection import DatabaseConnection
from database.database_utils import DatabaseUtils


class HttpUtils:
    code = {
        'success': '200 OK',
        'syntax_error': '400 Bad Request',
        'not_found': '404 Not Found'
    }

    type = {
        'json': 'application/json',
        'text': 'text/plain'
    }


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True


# if 'error' in dict.keys():
# print("value =", dict[error])
def parse_request(request):
    if is_json(request):
        return json.loads(request)
    else:
        return {'error': 'invalid json format'}


def format_response(status_code, content_type, response_body):
    return 'HTTP/1.1 {code}\r\nContent-Type: {type}\r\nContent-Length: {length}\r\n\r\n{body}' \
        .format(code=status_code, type=content_type,
                length=len(response_body), body=response_body)


def handle_error(conn, status_code, response_body):
    rp = format_response(status_code, HttpUtils.type['json'], response_body)
    conn.sendall(rp.encode('ASCII'))


db = DatabaseUtils(DatabaseConnection('localhost', 'root', '778899', 'greenhouse'))


def handle_request(conn, request):
    if 'value' in request.keys():
        sql = request['value']
        r = db.query(sql)
        conn.sendall(r)


def accept(sock, _mask):
    # conn is a new socket usable to send and receive data on the connection
    conn, addr = sock.accept()
    print('accepted', conn, 'from', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, handle_client)


def handle_client(conn, _mask):
    # The return value is a bytes object representing the data received.
    # The maximum amount of data to be received at once is specified by bufsize.
    # When a recv returns 0 bytes, it means the other side has closed the connection.
    data = conn.recv(1024)
    if data:
        print('received ', repr(data), 'from', conn.getpeername())
        response = 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: ' \
                   '{length}\r\n\r\n{body}'.format(length=len(body), body=body)
        conn.send(response.encode('ASCII'))
        # request = parse_request(data)
        # print('received ', repr(data), 'from', conn.getpeername())
        # if 'error' in request.keys():
        #     handle_error(conn, request)
        # else:
        #     handle_request(conn, request)
    sel.unregister(conn)
    conn.close()


sel = selectors.DefaultSelector()
listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    listen_sock.bind(('0.0.0.0', 8080))
except OSError as msg:
    print('sock.bind(): ' + str(msg))
    sys.exit()

listen_sock.listen(100)
listen_sock.setblocking(False)
# EVENT_READ Available for read
# EVENT_WRITE Available for write
sel.register(listen_sock, selectors.EVENT_READ, accept)

while True:
    # select() returns a list of (key, events) tuples, one for each ready file object.
    # key is the SelectorKey instance corresponding to a ready file object.
    # events is a bitmask of events ready on this file object.
    # A SelectorKey is a namedtuple used to associate a file object to its
    # underlying file descriptor, selected event mask and attached data.
    # You can register multiple events for a socket.
    # The reported mask will tell you which of those events is actually ready.
    events = sel.select()
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
