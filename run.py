from aonely import Aonely
from aonely.io_loop import IOLoop
from aonely.coroutine import coroutine
from aonely.app import request_stack
from aonely.client import Client

app = Aonely()
client = Client(app)


@app.route('/')
def index():
    return 'You are visiting %s' % index.__name__


@app.route('/get')
@coroutine
def get():
    response = yield from client.get('http://www.baidu.com')
    return response


if __name__ == '__main__':
    app.run()
    IOLoop.instance().start()
