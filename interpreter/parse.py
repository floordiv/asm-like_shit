import os
import sys

from pprint import pprint

import api
import function
import exception
import namespace


namespace = namespace.Namespace()


def parse_line(line, line_index='null', space='main'):
    line = remove_comments(line).strip()

    if line.strip() == '':
        return

    func, *line = line.split()

    if func == 'use':
        module_name = line[0]

        if module_name[0] == '"':
            *module_path, module_name = module_name[1:-1].split('/')
            module_path = '/'.join(module_path)

            load_module(module_name, (module_path,), line_index)
        else:
            load_module(module_name, on_line=line_index)

        return

    if len(func.split(':')) > 1:
        space, func = func.split(':')

    func = namespace.get(func, space=space)

    if func is None:
        return

    line = ' '.join(line)

    args, kwargs = parse_args(line, line_index, space=space)

    return api.call(func, args, kwargs, line_index, space)


def parse_lines(iter_obj, space='main'):
    function_initializing = False
    func_body_temp = {'name': None, 'args': (), 'kwargs': {}, 'body': [], 'func_ranges': ['null', 'null']}

    for index, line in enumerate(iter_obj, start=1):
        line = remove_comments(line).strip()

        if line == '':
            continue

        if line == 'end':
            function_initializing = False
            func_body_temp['func_ranges'][1] = index

            newfunc = function.Function(*func_body_temp.values(), api.get_functions())

            namespace.put(func_body_temp['name'], newfunc, space=space)

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
            parse_line(line, index, space)


def parse_args(args, line='null', replace_variables=True, space='main'):
    split_args = split(args)

    args, kwargs = [], {}

    next_arg_is_value = False

    for arg in split_args:
        if next_arg_is_value:
            if replace_variables:
                arg = checkvar(arg, line, space)

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
                    val = checkvar(val[0], line, space)

                kwargs[var] = val
            else:
                if replace_variables:
                    arg = checkvar(arg, line, space)

                args += [arg]

    return args, kwargs


def load_module(name, paths=('modules/', './', 'examples/'), on_line='null'):
    for path in paths:
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
                    parse_lines(module, space=name)

            return

    exception.throw('module_not_found', f'module not found: {name}', line=on_line)


def checkvar(var, on_line, space='main'):
    if var[0] == '&':
        return namespace.get(var[1:], True, on_line, space=space)

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
