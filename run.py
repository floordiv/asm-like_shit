import api
import sys
import shlex


class Namespace:
    def __init__(self):
        self.namespace = {}

    def add(self, var, val):
        self.namespace[var] = val

    def remove(self, var):
        del self.namespace[var]

    def get(self, var):
        return self.namespace.get(var)


def line_parser(line):
    line = shlex.split(line)

    func = line[0]
    args = line[1:]
    kwargs = {}

    for index, arg in enumerate(args):
        if '=' in arg:  # this is a kwarg
            var, *val = arg.split('=')

            kwargs[var] = '='.join(val)
            del args[index]

    return func, args, kwargs


if __name__ == '__main__':
    args = sys.argv[1:]
    namespace = Namespace()

    if len(args) == 0:
        print('Please, type a name of the file')

        sys.exit()

    file = args[0]

    with open(file, 'r') as source:
        source = source.read().splitlines()

    for line in source:
        func, args, kwargs = line_parser(line)

        response = api.__dict__[func](namespace, *args, **kwargs)

        if response is not None:
            if response.startswith('add_var:'):
                _, var, val = response.split(':')

                namespace.add(var, val)
