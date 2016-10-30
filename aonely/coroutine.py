from functools import wraps

from aonely.future import Future


class Task(object):
    def __init__(self, coro):
        self.coro = coro
        future = Future()
        future.set_result(None)
        self.step(future)

    def step(self, future):
        try:
            next_future = self.coro.send(future.result)
        except StopIteration:
            return
        next_future.add_callback(self.step)


def coroutine(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        return Task(fn(*args, **kwargs))

    return wrapper
