import sys
import time

interpreter_path = './interpreter'

if len(sys.argv) > 1:
    interpreter_path = ' '.join(sys.argv[1:])

sys.path.append(interpreter_path)

import interpreter.interpreter as lang


lang.exit_on_err(False)


try:
    while True:
        line = input('&> ')

        begin = time.time()

        result = lang.run_line(line)

        if result is not None:
            print(result)

        if '--benchmark' in sys.argv:
            print('Time went:', time.time() - begin, 'secs')
except KeyboardInterrupt:
    lang.run_line('exit reason="user aborted"')
