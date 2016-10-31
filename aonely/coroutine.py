from functools import wraps

from aonely.future import Future


class Task(object):
    def __init__(self, generator):
        self.generator = generator
        future = Future()
        future.set_result(None)
        self.step(future)

    def step(self, future):
        try:
            next_future = self.generator.send(future.result)
        except StopIteration:
            return
        next_future.add_callback(self.step)


def asyncio(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        return Task(fn(*args, **kwargs))

    return wrapper


def _generator():
    yield


TYPE_GENERATOR = type(_generator())
