import exception


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)

        return instances[class_]

    return getinstance


@singleton
class Namespace:
    def __init__(self, init_vars=None, **kwargs):
        if init_vars is None:
            init_vars = {}

        self.variables = {**init_vars, **kwargs}

    def get(self, var, throw=True, line='null'):
        if not throw:
            return self.variables.get(var)

        try:
            return self.variables[var]
        except KeyError:
            exception.throw('variable_not_found', 'variable not found: "' + str(var) + '"', line=line)

    def put(self, var, val):
        self.variables[var] = val

    def rm(self, var, line='null'):
        try:
            del self.variables[var]
        except KeyError:
            exception.throw('variable_not_found', 'variable not found: "' + str(var) + '"', line=line)

    def load_variables(self, variables):
        self.variables = {**self.variables, **variables}

    def get_variables(self):
        return self.variables

    def __contains__(self, item):
        return item in self.variables

    def __str__(self):
        return '\n'.join([f'{a}: {b}' for a, b in self.variables.items()])


class LocalNamespace:
    def __init__(self, init_vars=None, **kwargs):
        if init_vars is None:
            init_vars = {}

        self.variables = {**init_vars, **kwargs}

    def get(self, var, throw=True, line='null'):
        if not throw:
            return self.variables.get(var)

        try:
            return self.variables[var]
        except KeyError:
            exception.throw('variable_not_found', 'variable not found: "' + str(var) + '"', line=line)

    def put(self, var, val):
        self.variables[var] = val

    def rm(self, var):
        try:
            del self.variables[var]
        except KeyError:
            exception.throw('variable_not_found', 'variable not found: "' + str(var) + '"')

    def load_variables(self, variables):
        self.variables = {**self.variables, **variables}

    def __contains__(self, item):
        return item in self.variables

    def __str__(self):
        return '\n'.join([f'{a}: {b}' for a, b in self.variables.items()])
