import parse
import namespace


global_namespace = namespace.Namespace()


class Function:
    def __init__(self, name, args, kwargs, funcbody, lines_range=('null', 'null'), api_functions=None):
        if api_functions is None:
            api_functions = {}

        self.api_functions = api_functions
        self.name = name
        self.args, self.kwargs = args, kwargs

        if 'null' not in lines_range:
            self.lines_range = list(range(lines_range[0], lines_range[1] + 1))
        else:
            self.lines_range = ['null'] * len(funcbody)

        self.funcbody = list(zip(self.lines_range, funcbody))

    def __call__(self, *args, **kwargs):
        args = dict(zip(self.args, args))

        local_namespace = namespace.LocalNamespace({**args, **kwargs, **self.api_functions})

        for line_index, line in self.funcbody:
            parse.parse_line(line, line_index, local_namespace)

        del local_namespace
