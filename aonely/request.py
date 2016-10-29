class Request(object):
    def __init__(self, env):
        headers = env.decode().split('\r\n\r\n')[0].split('\r\n')
        method, path, protocol = headers.pop(0).split(' ')

        self.args = {}
        if '?' in path:
            path, params = path.split('?')
            if params:
                params = params.split('&')
                for param in params:
                    arg, value = param.split('=')
                    self.args[arg] = value

        self.method = method
        self.path = path
        self.protocol = protocol

        for header in headers:
            attr, value = header.split(':', 1)
            self.__setattr__(attr, value.strip())
