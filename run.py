import api
import sys
import shlex


IGNORE_ERRORS = False


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
    if line.replace(' ', '') == '' or line.startswith('//'):
        # an empty line
        return

    line = shlex.split(line)

    if '//' in line:
        line = line[:line.index('//')]

    func = line[0]
    args = line[1:]
    kwargs = {}

    for index, arg in enumerate(args):
        # if ' ' not in arg - whether // is not in the text
        if '//' in arg and ' ' not in arg:  # remove comment
            arg = arg.split('//')[0]
            args[index] = arg
            del args[index:]    # delete everything after comment beginning

        if arg == '':
            continue

        if '=' in arg:  # this is a kwarg
            var, *val = arg.split('=')

            kwargs[var] = '='.join(val)
            del args[index]

    return func, args, kwargs


def start_interpreting(namespace, args):
    if len(args) == 0:
        print('Please, type a name of the file')

        sys.exit()

    file = args[0]

    with open(file, 'r') as source:
        source = source.read().splitlines()

    for index, line in enumerate(source):
        line = line_parser(line)

        if line is None:
            continue

        func, args, kwargs = line

        # print(args, kwargs)

        response = str(api.__dict__[func](namespace, *args, **kwargs))

        if response is not None:
            if response.startswith('add_var:'):
                _, var, val = response.split(':')

                namespace.add(var, val)
            elif response.startswith('error:'):
                err_text = ':'.join(response.split(':')[1:])

                print('ERROR on line {line}: {err_text}'.format(line=index + 1, err_text=err_text))

                if not IGNORE_ERRORS:
                    sys.exit()


if __name__ == '__main__':
    start_interpreting(Namespace(), sys.argv[1:])

