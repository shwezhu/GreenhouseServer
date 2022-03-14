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


def parse_request(request):
    raw_list = request.split("\r\n")
    request = {}
    for index in range(1, len(raw_list)):
        item = raw_list[index].split(":")
        if len(item) == 2:
            request.update({item[0].lstrip(' '): item[1].lstrip(' ')})
    return request


def format_response(status_code, content_type, response_body):
    return 'HTTP/1.1 {code}\r\nContent-Type: {type}\r\nContent-Length: {length}\r\n\r\n{body}' \
        .format(code=status_code, type=content_type,
                length=len(response_body.encode('utf-8')), body=response_body)


def handle_error(conn, status_code, response_body):
    response_body = json.dumps({'error': response_body})
    rp = format_response(status_code, 'application/json', response_body)
    conn.sendall(rp.encode('utf-8'))


db = DatabaseUtils(DatabaseConnection('localhost', 'root', '778899', 'greenhouse'))


def handle_request(conn, sql):
    result = db.query(sql)
    conn.sendall(format_response('200 OK', 'application/json', result).encode('utf-8'))


def accept(sock, _mask):
    # conn is a new socket usable to send and receive data on the connection
    conn, addr = sock.accept()
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, handle_client)


def handle_client(conn, _mask):
    # The return value is a bytes object representing the data received.
    # The maximum amount of data to be received at once is specified by bufsize.
    # When a recv returns 0 bytes, it means the other side has closed the connection.
    raw_request = conn.recv(1024).decode('utf-8')
    if raw_request:
        request = parse_request(raw_request)
        if 'sql' in request.keys():
            print('received', str(request.get('sql')), 'from', conn.getpeername())
            handle_request(conn, request.get('sql'))
        else:
            handle_error(conn, '400 Bad Request', 'No sql parameter in headers.')
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
