import api
import function
import exception
import namespace


namespace = namespace.Namespace()


def parse_line(line, line_index='null', use_namespace=namespace):
    line = remove_comments(line).strip()

    if line.strip() == '':
        return

    args, kwargs = parse_args(line, line_index, use_namespace=use_namespace)

    func, *args = args

    return api.call(func, args, kwargs, line_index, use_namespace)


def parse_lines(iter_obj, use_namespace=namespace):
    function_initializing = False
    func_body_temp = {'name': None, 'args': (), 'kwargs': {}, 'body': [], 'func_ranges': ['null', 'null']}

    for index, line in enumerate(iter_obj, start=1):
        if line.strip() == '':
            continue

        if line.strip() == 'end':
            function_initializing = False
            func_body_temp['func_ranges'][1] = index

            newfunc = function.Function(*func_body_temp.values(), api.get_functions())
            use_namespace.put(func_body_temp['name'], newfunc)

            func_body_temp = {'name': None, 'args': (), 'kwargs': {}, 'body': [], 'func_ranges': ['null', 'null']}

        elif function_initializing:
            func_body_temp['body'] += [line]

        elif line[0] == '.':  # function init
            function_initializing = True
            func_body_temp['func_ranges'][0] = index

            new_func_name = line.split()[0][1:]
            args, kwargs = parse_args(line[len(new_func_name) + 1:], index, False)

            func_body_temp['name'] = new_func_name
            func_body_temp['args'] = args
            func_body_temp['kwargs'] = kwargs

        else:
            parse_line(line, index, use_namespace)


def parse_args(args, line='null', replace_variables=True, use_namespace=namespace):
    split_args = split(args)

    args, kwargs = [], {}

    next_arg_is_value = False

    for arg in split_args:
        if next_arg_is_value:
            if replace_variables:
                arg = checkvar(arg, line, use_namespace)

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
                    val = checkvar(val[0], line, use_namespace)

                kwargs[var] = val
            else:
                if replace_variables:
                    arg = checkvar(arg, line, use_namespace)

                args += [arg]

    return args, kwargs


def checkvar(var, on_line, use_namespace=namespace):
    if var[0] in ['"', '&'] or var.isdigit():
        return var

    return use_namespace.get(var, True, on_line)


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
