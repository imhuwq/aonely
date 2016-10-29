import threading

from selectors import DefaultSelector


class IOLoop(object):
    selector = DefaultSelector()

    _instance_lock = threading.Lock()
    _current = threading.local()

    @staticmethod
    def instance():
        if not hasattr(IOLoop, '_instance'):
            with IOLoop._instance_lock:
                if not hasattr(IOLoop, '_instance'):
                    IOLoop._instance = IOLoop()

        return IOLoop._instance

    def start(self):
        while True:
            events = self.selector.select()
            for key, mask in events:
                callback = key.data
                callback(key, mask)
