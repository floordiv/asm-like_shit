import os

import api
import function
import exception
import namespace


namespace = namespace.Namespace()


def parse_line(line, line_index='null', to_space='main'):
    line = remove_comments(line).strip()

    if line.strip() == '':
        return

    func, *line = line.split()

    if func == 'use':
        module_name = line[0]

        load_module(module_name)

        return

    func = namespace.get(func, from_space=to_space)

    if func is None:
        return

    line = ' '.join(line)

    args, kwargs = parse_args(line, line_index, from_space=to_space)

    return api.call(func, args, kwargs, line_index)


def parse_lines(iter_obj, to_space='main'):
    function_initializing = False
    func_body_temp = {'name': None, 'args': (), 'kwargs': {}, 'body': [], 'func_ranges': ['null', 'null']}

    for index, line in enumerate(iter_obj, start=1):
        line = line.strip()

        if line == '':
            continue

        if line == 'end':
            function_initializing = False
            func_body_temp['func_ranges'][1] = index

            newfunc = function.Function(*func_body_temp.values(), api.get_functions())

            namespace.put(func_body_temp['name'], newfunc, to_space=to_space)

            func_body_temp = {'name': None, 'args': (), 'kwargs': {}, 'body': [], 'func_ranges': ['null', 'null']}

        elif function_initializing:
            func_body_temp['body'] += [line]

        elif line[0] == '.':  # function init
            function_initializing = True
            func_body_temp['func_ranges'][0] = index

            new_func_name = line.split()[0][1:]
            args, kwargs = parse_args(line[len(new_func_name) + 2:], index, False)

            func_body_temp['name'] = new_func_name
            func_body_temp['args'] = args
            func_body_temp['kwargs'] = kwargs

        else:
            parse_line(line, index, to_space)


def parse_args(args, line='null', replace_variables=True, from_space='main'):
    split_args = split(args)

    args, kwargs = [], {}

    next_arg_is_value = False

    for arg in split_args:
        if next_arg_is_value:
            if replace_variables:
                arg = checkvar(arg, line, from_space)

            arg = arg.strip('"')

            kwargs[next_arg_is_value] = arg

            next_arg_is_value = False

        elif arg[0] == '"':
            args += [arg[1:-1]]
        else:
            if arg[-1] == '=':
                next_arg_is_value = arg[:-1]
            elif '=' in arg:
                var, *val = arg.split('=')

                if replace_variables:
                    val = checkvar(val[0], line, from_space)

                kwargs[var] = val
            else:
                if replace_variables:
                    arg = checkvar(arg, line, from_space)

                args += [arg]

    return args, kwargs


def load_module(name, on_line='null'):
    paths = ['modules/', './', 'examples/']

    for path in paths:
        if name in os.listdir(path):
            with open(path + name) as module:
                parse_lines(module, to_space=name)

            return

    exception.throw('module_not_found', f'module not found: {name}', line=on_line)


def checkvar(var, on_line, from_space='main'):
    if var[0] == '&':
        return namespace.get(var[1:], True, on_line, from_space=from_space)

    return var


def split_by_quotes(line, on_line='null'):
    result = ['']

    temp = []
    in_string = False

    for letter in line:
        if letter == '"':
            temp += [letter]

            if in_string:
                result += [''.join(temp), '']

                temp = []
                in_string = False
            else:
                in_string = True

        elif in_string:
            temp += [letter]
        else:
            result[-1] += letter

    if in_string:   # unclosed quote
        exception.throw('unclosed_quote', f'Unclosed quote: {"".join(temp)}  <-', line=on_line)

    return list(filter(lambda _element: _element != '', result))


def split(line, split_by=' ', on_line='null'):
    result = ['']
    line = remove_comments(line)

    for element in split_by_quotes(line, on_line=on_line):
        if element[0] == '"':
            result += [element, '']
        else:
            for letter in element.strip():
                if letter == split_by:
                    result += ['']
                else:
                    result[-1] += letter

    return list(filter(lambda _element: _element != '', result))


def remove_comments(line):
    in_string = False

    for index, letter in enumerate(line):
        if letter == '"':
            in_string = not in_string
        elif not in_string and letter == ';':
            return line[:index]

    return line
