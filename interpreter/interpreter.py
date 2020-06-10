import sys

import api
import parse
import exception
import namespace


namespace = namespace.Namespace()  # add all the api functions as a variable values
namespace.load_variables(api.get_functions())


def run(file):
    with open(file) as source:
        for index, line in enumerate(source, start=1):
            parse.parse_line(line, line_index=index)


def run_line(line):
    return parse.parse_line(line, line_index=0)


def run_lines(lines):
    for index, line in enumerate(lines, start=1):
        parse.parse_line(line, line_index=index)


def exit_on_err(value=True):
    exception.EXIT_ON_EXCEPTION = value


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('USAGE: python3 interpreter.py <filename>, where filename - file, which should be executed')

        sys.exit()

    source_file = sys.argv[1]

    run(source_file)
