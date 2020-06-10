import os

import coloredoutput


EXIT_ON_EXCEPTION = True


err_format = 'ERROR: {errtype}\nLINE: {line}\nDESCRIPTION: {errdesc}'


def throw(errtype, *errdesc, line='null', color='red'):
    # 13
    errdesc = '\n'.join([errdesc[0]] + [' ' * 13 + str(element) for element in errdesc[1:]])

    print(coloredoutput.colorit(err_format.format(errtype=errtype,
                                                  errdesc=errdesc,
                                                  line=line),
                                color))

    if EXIT_ON_EXCEPTION:
        os.abort()
