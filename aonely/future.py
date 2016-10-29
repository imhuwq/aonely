class Future(object):
    def __init__(self):
        self.result = None
        self._callbacks = []

    def add_callback(self, callback):
        self._callbacks.append(callback)

    def set_result(self, result):
        self.result = result
        for callback in self._callbacks:
            callback(self)

    def __iter__(self):
        yield self
        return self.result
