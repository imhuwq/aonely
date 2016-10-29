from functools import wraps

from aonely.server import Server
from aonely.coroutine import Task


class DuplicatedHander(BaseException):
    pass


class Aonely(object):
    def __init__(self):
        self.server = None
        self._handlers = {}

    def route(self, url):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            existed_handler = self._handlers.get('url')
            if existed_handler:
                raise DuplicatedHander('You are registering duplicated handler to the same url: %s' % url)
            self._handlers[url] = func
            return wrapper

        return decorator

    def dispatch_request(self, request):
        path = request.path
        handler = self._handlers.get(path, None)
        if handler:
            response = handler()
        else:
            response = 'Not Found'
        return response.encode()

    def run(self, host='0.0.0.0', port=5000):
        self.server = Server(host, port, self)
        self.server.start()
