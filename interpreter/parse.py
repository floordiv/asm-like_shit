import api
import exception
import namespace


namespace = namespace.Namespace()


def parse_line(line, line_index='null'):
    args, kwargs = parse_args(line, line_index)

    func, *args = args

    return api.call(func, args, kwargs, line_index)


def parse_args(args, line='null'):
    split_args = split(args)

    args, kwargs = [], {}

    next_arg_is_value = False

    for arg in split_args:
        if next_arg_is_value:
            arg = checkvar(arg, line)

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

                val = checkvar(val[0], line)

                kwargs[var] = val
            else:
                arg = checkvar(arg, line)

                args += [arg]

    return args, kwargs


def checkvar(var, on_line):
    if var[0] in ['"', '&'] or var.isdigit():
        return var

    return namespace.get(var, True, on_line)


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
