import exception


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)

        return instances[class_]

    return getinstance


def var_from(var):
    var = var.split(':')

    if len(var) == 1:
        return 'main', var[0]
    return var


@singleton
class Namespace:
    def __init__(self, init_vars=None, **kwargs):
        if init_vars is None:
            init_vars = {}

        self.variables = {'main': {**init_vars, **kwargs}}

    def get(self, var, throw=True, line='null', space='main'):
        try:
            return self.variables[space][var]
        except KeyError:
            if throw:
                exception.throw('variable_not_found', f'variable not found: {space}:{var}', line=line)

    def put(self, var, val, space='main'):
        if space not in self.variables:
            self.create_space(space)

        self.variables[space][var] = val

    def rm(self, var, line='null', space='main'):
        try:
            del self.variables[space][var]
        except KeyError:
            exception.throw('variable_not_found', f'variable not found: {space}:{var}', line=line)

    def load_variables(self, variables, space='main'):
        self.variables[space] = {**self.variables, **variables}

    def get_variables(self, space='main'):
        return self.variables[space]

    def create_space(self, newspace):
        self.variables[newspace] = self.variables['main']

    def __contains__(self, item):
        return item in self.variables

    def __str__(self):
        return '\n'.join([f'{a}: {b}' for a, b in self.variables.items()])
