import re
import socket
from selectors import EVENT_READ, EVENT_WRITE

from aonely.io_loop import IOLoop
from aonely.future import Future


class Client(object):
    connections = {}
    requests = {}
    responses = {}

    def __init__(self, app=None):
        self.io_loop = IOLoop().instance()
        self.selector = self.io_loop.selector
        self.app = app

    def get(self, url):
        if not re.match(r'^(https?://)', url):
            url = 'http://' + url
        url_segs = [seg for seg in re.split('(https?)://|/{1}', url, 2) if seg]
        if len(url_segs) == 2:
            url_segs.append('/')
        protocol, host, path = url_segs
        port = 80 if protocol == 'http' else 443

        connection = socket.socket()
        connection.setblocking(False)
        try:
            connection.connect((host, port))
        except BlockingIOError:
            pass

        future = Future()

        def on_writable(key, mask):
            future.set_result(None)

        self.selector.register(connection.fileno(), EVENT_WRITE, on_writable)

        yield from future

        self.selector.unregister(connection.fileno())

        request = 'GET {} HTTP/1.0\r\nHost: {}\r\n\r\n'.format(url, host)
        connection.send(request.encode('ascii'))

        def read(sock):
            f = Future()

            def on_readable(key, mask):
                f.set_result(sock.recv(4096))

            self.selector.register(sock.fileno(), EVENT_READ, on_readable)

            chunk = yield from f
            self.selector.unregister(sock.fileno())
            return chunk

        def read_all(sock):
            response = []
            chunk = yield from read(sock)
            while chunk:
                response.append(chunk)
                chunk = yield from read(sock)
            return b''.join(response)

        response = yield from read_all(connection)
        return response
