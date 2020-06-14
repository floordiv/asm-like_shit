import sys
import string

import exception
import namespace


namespace = namespace.Namespace()
self = sys.modules[__name__]

bool_vars = {
    'true': True,
    'false': False,
    '1': True,
    '0': False,
}


def out(*text, line='null', **kwargs):
    spaces = ''

    if 'space' in kwargs:
        del kwargs['space']
    if 'spaces' in kwargs:
        spaces = kwargs['spaces']
        del kwargs['spaces']

    text = spaces.join(map(str, text))

    print(text, **kwargs)


def inp(to_var=None, text=None, line='null', space='main'):
    if to_var is None:
        text = ''
    elif text is None:
        text = to_var
    else:
        to_var = to_var

    text = input(text)

    if to_var is not None:
        namespace.put(to_var, text, space)

    return text.replace('"', '\\"')


def var(varname=None, *content, line='null', space='main'):
    if varname is None:
        return

    if len(content) == 1:
        content = content[0]

    namespace.put(varname, content, space)


def call(func, args=(), kwargs=None, line='null', space='main'):
    if kwargs is None:
        kwargs = {}

    try:

        if callable(func):  # if we have a function object (not it's name)
            # I commented a code below, because external modules can take these parameters

            # is_external = namespace.get('external_module', False, line, space)
            #
            # if is_external is None:
            #     kwargs['line'] = line
            #     kwargs['space'] = space

            function = func(*args, line=line, space=space, **kwargs)
        else:
            function = getattr(self, func)(*args, line=line, space=space, **kwargs)
    except Exception as exc:
        exception.throw('call_failure', f'failed to call {func} from namespace {space}: {exc}')

        return

    return function


def seq(to_var=None, sequence=None, line='null', space='main'):
    if to_var is None:
        return

    if sequence is None:
        sequence = to_var
        to_var = None

    if any([i in string.ascii_letters.replace('e', '') for i in sequence]):
        exception.throw('bad_sequence', f'bad sequence: {sequence}  <-', line=line)

        return

    try:
        result = eval(sequence)

        if to_var is not None:
            namespace.put(to_var, result, space=space)
    except Exception as exc:
        exception.throw('bad_sequence', 'bad sequence:', exc, line=line)


def pass_line(*args, **kwargs):
    return


def delvar(*variables, line='null', space='main'):
    for variable in variables:
        namespace.rm(variable, line=line, space=space)


def exit_(code=None, reason=None, line='null', space='main'):
    print('\nAborted', '(' + str(reason) + ')' if reason is not None else '')

    try:
        sys.exit(int(code))
    except (ValueError, TypeError):
        sys.exit(1)


def set_immortality(value, line='null', space='main'):
    try:
        exception.EXIT_ON_EXCEPTION = not bool_vars[value]
    except KeyError:
        exception.throw('bad_state', 'unknown value for function "setimm": ' + str(value), line=line)


function_map = {
        'out': out,
        'inp': inp,
        'in': inp,
        'var': var,
        'call': call,
        'seq': seq,
        'del': delvar,
        'pass': pass_line,
        'exit': exit_,
        'imm': set_immortality,
}


def get_functions():
    return function_map


def addcmd(funcmap):
    function_map.update(funcmap)


def compare(variables):
    for variable, value in variables.items():
        if variable not in self.__dict__:
            self.__dict__[variable] = value
