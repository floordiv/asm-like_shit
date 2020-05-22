def out(namespace, *text, **kwargs):
    text = list(text)

    for index, element in enumerate(text):
        if element.startswith('&'):
            variable = namespace.get(element[1:])

            if variable is None:
                return 'error:variable not found'

            text[index] = variable

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
