import selectors


class SocketConnection:
    sel = selectors.DefaultSelector()

    @staticmethod
    def accept(sock, mask):
        # conn is a new socket usable to send and receive data on the connection
        conn, addr = sock.accept()
        print('accepted', conn, 'from', addr)
        conn.setblocking(False)
        sock.sel.register(conn, selectors.EVENT_READ, SocketConnection.handle_client)

    @staticmethod
    def handle_client(conn, mask):
        # The return value is a bytes object representing the data received.
        # The maximum amount of data to be received at once is specified by bufsize.
        # When a recv returns 0 bytes, it means the other side has closed the connection.
        request = conn.recv(100)
        if request:
            print('echoing', repr(request), 'to', conn.getpeername())

            conn.send(request)
        SocketConnection.sel.unregister(conn)
        conn.close()
