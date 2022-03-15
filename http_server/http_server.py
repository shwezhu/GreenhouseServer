import json
import selectors
import socket
import sys
import logging


class HTTPServer:
    sel = selectors.DefaultSelector()

    def __init__(self, addr, port, database_connection):
        self._db = database_connection
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__init(addr, port)

    def __init(self, addr, port=8080):
        try:
            self._sock.bind((addr, port))
        except OSError as err:
            logging.fatal(str(err) + ' in HTTPServer.__init method')
            sys.exit()
        self._sock.listen(200)
        self._sock.setblocking(False)
        self.sel.register(self._sock, selectors.EVENT_READ, self.__accept)

    def __accept(self, sock, _mask):
        # conn is a new socket usable to send and receive data on the connection
        conn, addr = sock.accept()
        conn.setblocking(False)
        self.sel.register(conn, selectors.EVENT_READ, self.__handle_client)

    def __handle_client(self, conn, _mask):
        # The return value is a bytes object representing the data received.
        # The maximum amount of data to be received at once is specified by bufsize.
        # When a recv returns 0 bytes, it means the other side has closed the connection.
        raw_request = conn.recv(1024).decode('utf-8')
        if raw_request:
            request = self.parse_request(raw_request)
            if 'sql' in request.keys():
                print('received', str(request.get('sql')), 'from', conn.getpeername())
                self.handle_request(conn, request.get('sql'))
            else:
                self.handle_error(conn, '400 Bad Request', 'No sql parameter in headers.')
        self.sel.unregister(conn)
        conn.close()

    @staticmethod
    def parse_request(request):
        raw_list = request.split("\r\n")
        request = {}
        for index in range(1, len(raw_list)):
            item = raw_list[index].split(":")
            if len(item) == 2:
                request.update({item[0].lstrip(' '): item[1].lstrip(' ')})
        return request

    @staticmethod
    def format_response(status_code, content_type, response_body):
        return 'HTTP/1.1 {code}\r\nContent-Type: {type}\r\nContent-Length: {length}\r\n\r\n{body}' \
            .format(code=status_code, type=content_type,
                    length=len(response_body.encode('utf-8')), body=response_body)

    @staticmethod
    def handle_error(conn, status_code, response_body):
        response_body = json.dumps({'error': response_body})
        rp = HTTPServer.format_response(status_code, 'application/json', response_body)
        conn.sendall(rp.encode('utf-8'))

    def handle_request(self, conn, sql):
        result = self.__query(conn=conn, sql=sql)
        if result is None:
            return None
        conn.sendall(HTTPServer.format_response('200 OK', 'application/json', result).encode('utf-8'))

    def __query(self, conn, sql, params=None):
        raw_results = self._db.query(conn=conn, sql=sql, params=params)
        if raw_results is None:
            return None
        row_header = [d[0] for d in self._db.cursor.description]
        data = []
        for r in raw_results:
            data.append(dict(zip(row_header, r)))
        json.dumps(data, indent=4, sort_keys=True, default=str)
        results = json.dumps({'results': data})
        return results

    def __execute(self, conn, sql, params=None):
        self._db.execute(sql=sql, conn=conn, params=params)
