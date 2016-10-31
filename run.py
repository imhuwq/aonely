from aonely import Aonely
from aonely.io_loop import IOLoop

app = Aonely()


@app.route('/')
def index():
    return 'You are visiting %s' % index.__name__


@app.route('/baidu')
def baidu():
    response = yield from app.client.get('http://www.baidu.com/')
    return response


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8888)
    IOLoop.instance().start()
