import string


def detect_vars(namespace, text):
    for index, element in enumerate(text):
        if element.startswith('&'):
            variable = namespace.get(element[1:])

            if variable is None:
                return 'error:variable not found: ' + element[1:]

            text[index] = variable

    return text


def out(namespace, *text, **kwargs):
    text = detect_vars(namespace, list(text))

    if isinstance(text, str):   # detect_vats should always return list, otherwise we have an error
        return text

    print(*text, **kwargs)


def inp(namespace, text, to_var=None):
    if text.startswith('&'):
        text = namespace.get(text[1:])

    text = input(text)

    if to_var is not None:
        text = 'add_var:' + to_var + ':' + text

    return text


def var(namespace, varname, *content):
    namespace.add(varname, ' '.join(content))


def add(namespace, to_var, num1, num2):
    num1, num2 = detect_vars(namespace, [num1, num2])

    result = int(num1) + int(num2)

    namespace.add(to_var, result)

    return result


def seq(namespace, *sequence):
    sequence = ' '.join(sequence)

    if any([i in string.ascii_letters.replace('e', '') for i in sequence]):
        return 'error:bad sequence'

    try:
        return eval(sequence)
    except Exception as exc:
        return 'error:bad sequence: ' + str(exc)
