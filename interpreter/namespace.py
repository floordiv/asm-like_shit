import exception


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)

        return instances[class_]

    return getinstance


def var_from(var):
    var = var.split('.')

    if len(var) == 1:
        return 'global', var[0]
    return var


@singleton
class Namespace:
    def __init__(self, init_vars=None, **kwargs):
        if init_vars is None:
            init_vars = {}

        self.variables = {'global': {**init_vars, **kwargs}}

    def get(self, var, throw=True, line='null'):
        from_space, var = var_from(var)

        if not throw:
            return self.variables[from_space].get(var)

        try:
            return self.variables[from_space][var]
        except KeyError:
            exception.throw('variable_not_found', f'variable not found: {from_space}.{var}', line=line)

    def put(self, var, val, to_space='global'):
        from_space, var = var_from(var)

        self.variables[to_space][var] = val

    def rm(self, var, line='null'):
        from_space, var = var_from(var)

        try:
            del self.variables[from_space][var]
        except KeyError:
            exception.throw('variable_not_found', f'variable not found: {from_space}.{var}', line=line)

    def load_variables(self, variables, to_space='global'):
        self.variables[to_space] = {**self.variables, **variables}

    def get_variables(self, from_space='global'):
        return self.variables[from_space]

    def __contains__(self, item):
        return item in self.variables

    def __str__(self):
        return '\n'.join([f'{a}: {b}' for a, b in self.variables.items()])


class LocalNamespace:
    def __init__(self, init_vars=None, **kwargs):
        if init_vars is None:
            init_vars = {}

        self.variables = {'global': {**init_vars, **kwargs}}

    def get(self, var, throw=True, line='null'):
        from_space, var = var_from(var)

        if not throw:
            return self.variables[from_space].get(var)

        try:
            return self.variables[from_space][var]
        except KeyError:
            exception.throw('variable_not_found', f'variable not found: {from_space}.{var}', line=line)

    def put(self, var, val, to_space='global'):
        from_space, var = var_from(var)

        self.variables[to_space][var] = val

    def rm(self, var, line='null'):
        from_space, var = var_from(var)

        try:
            del self.variables[from_space][var]
        except KeyError:
            exception.throw('variable_not_found', f'variable not found: {from_space}.{var}', line=line)

    def load_variables(self, variables, to_space='global'):
        self.variables[to_space] = {**self.variables, **variables}

    def get_variables(self, from_space='global'):
        return self.variables[from_space]

    def __contains__(self, item):
        return item in self.variables

    def __str__(self):
        return '\n'.join([f'{a}: {b}' for a, b in self.variables.items()])
