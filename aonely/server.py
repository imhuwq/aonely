import socket
from selectors import EVENT_READ, EVENT_WRITE

from aonely.io_loop import IOLoop
from aonely.coroutine import asyncio
from aonely.request import Request

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'


class Server(object):
    clients = {}
    requests = {}
    responses = {}

    def __init__(self, app=None, host='0.0.0.0', port=5000):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversocket.bind((host, port))
        serversocket.listen()
        serversocket.setblocking(0)

        self.socket = serversocket
        self.io_loop = IOLoop().instance()
        self.selector = self.io_loop.selector
        self.app = app

    def serve(self):

        def on_accessible(key, mask):
            client, address = self.socket.accept()
            client.setblocking(0)
            self.selector.register(client.fileno(), EVENT_READ, on_readable)
            self.clients[client.fileno()] = client
            self.requests[client.fileno()] = b''

        @asyncio
        def on_readable(key, mask):
            self.requests[key.fd] += self.clients[key.fd].recv(4096)
            if EOL1 in self.requests[key.fd] or EOL2 in self.requests[key.fd]:
                request_env = self.requests[key.fd]
                request = Request(request_env)
                self.responses[key.fd] = yield from self.app.dispatch_request(request)
                self.selector.modify(key.fd, EVENT_WRITE, on_writable)

        def on_writable(key, mask):
            byteswritten = self.clients[key.fd].send(self.responses[key.fd])
            self.responses[key.fd] = self.responses[key.fd][byteswritten:]
            print('sending to %s %s bytes data' % (key.fd, byteswritten))
            if len(self.responses[key.fd]) == 0:
                self.selector.unregister(key.fd)
                self.clients[key.fd].close()
                del self.clients[key.fd]

        self.selector.register(self.socket.fileno(), EVENT_READ, on_accessible)

    def start(self):
        self.serve()
