from aonely import Aonely
from aonely.io_loop import IOLoop
from aonely.coroutine import Task

app = Aonely()


@app.route('/')
def index():
    return 'You are visiting %s' % index.__name__


if __name__ == '__main__':
    app.run()
    IOLoop.instance().start()
