try:
    from termcolor import colored

    colors = True
except ImportError:
    colors = False


def colorit(text, color, **kwargs):
    if not colors:
        return text

    return colored(text, color, **kwargs)
