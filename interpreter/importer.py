import os
import sys

import namespace
import exception

namespace = namespace.Namespace()


PATHS = ['./', 'modules/', 'examples/', *sys.path]


def load_module(handler, name, bypath=None, on_line='null'):
    if bypath is None:
        for path in PATHS:
            if not path.endswith('/'):
                path += '/'

            if name in os.listdir(path):
                if name.endswith('.py'):
                    name = name[:-3]  # remove .py in the end

                    sys.path.append(path)

                    module = __import__(name)

                    namespace.create_space(name)
                    namespace.load_variables(module.__dict__, name)

                    namespace.put('external_module', True, name)
                else:
                    with open(path + name) as module:
                        handler(module, space=name)

                return
    else:
        sys.path.append(bypath)

        try:
            return __import__(name)
        except ModuleNotFoundError:
            pass    # an exception will be raised anyway

    exception.throw('module_not_found', f'module not found: {name}', line=on_line)
