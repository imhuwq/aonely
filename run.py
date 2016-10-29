from aonely import Aonely
from aonely.io_loop import IOLoop
from aonely.app import request_stack

app = Aonely()


@app.route('/')
def index():
    return 'You are visiting %s' % index.__name__


@app.route('/get')
def get():
    request = request_stack.pop()
    page = request.args.get('page', 'no page specified')
    return page


if __name__ == '__main__':
    app.run()
    IOLoop.instance().start()
