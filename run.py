import sys

sys.path.append('interpreter/')

if '/' in sys.argv[0]:
    sys.path.append(sys.argv[0])

import interpreter.interpreter as lang


file = sys.argv[1]

lang.run(file)
