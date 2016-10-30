import threading
from functools import wraps

from aonely.client import Client
from aonely.server import Server


class DuplicatedHandler(BaseException):
    pass


def generator():
    yield


type_generator = type(generator())


class RequestStack(object):
    def __init__(self):
        self.data = list()

    def push(self, item):
        self.data.append(item)

    def pop(self):
        return self.data.pop() if self.data else None


class Aonely(object):
    _request_stack_lock = threading.Lock()

    def __init__(self):
        self.server = None
        self.client = None
        self._handlers = {}

    @staticmethod
    def request_stack():
        if not hasattr(Aonely, '_request_stack'):
            with Aonely._request_stack_lock:
                if not hasattr(Aonely, '_request_stack'):
                    Aonely._request_stack = RequestStack()

        return Aonely._request_stack

    def route(self, url):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            existed_handler = self._handlers.get('url')
            if existed_handler:
                raise DuplicatedHandler('You are registering duplicated handler to the same url: %s' % url)
            self._handlers[url] = func
            return wrapper

        return decorator

    def dispatch_request(self, request_env):
        self.request_stack().push(request_env)
        handler = self._handlers.get(request_env.path, None)
        if handler:
            response = handler()
            if type(response) == type_generator:
                response = yield from response
        else:
            response = 'Not Found'

        try:
            response = response.encode()
        except AttributeError:
            pass

        return response

    def run(self, host='0.0.0.0', port=5000):
        self.client = Client(self)
        self.server = Server(self, host, port)
        self.server.start()


request_stack = Aonely.request_stack()
