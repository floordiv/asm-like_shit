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
    if 'space' in kwargs:
        del kwargs['space']

    text = ''.join(map(str, text))

    print(''.join(text), **kwargs)

    # return ' '.join(text)


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

    if callable(func):  # if we have a function object (not it's name)
        function = func(*args, line=line, space=space, **kwargs)
    else:
        function = getattr(self, func)(*args, line=line, space=space, **kwargs)

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


def get_functions():
    return {
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
