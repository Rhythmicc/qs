import json
import sys
import os

dir_char = '\\' if sys.platform.startswith('win') else '/'
user_root = os.path.expanduser('~')
if os.path.exists(user_root + dir_char + '.qsrc'):
    with open(user_root + dir_char + '.qsrc', 'r') as f:
        qsconfig = json.loads(f.read())
else:
    with open(user_root + dir_char + '.qsrc', 'w') as f:
        f.write('{\n'
                '  "rmbg": "GET API KEY: https://www.remove.bg"\n'
                '  "smms": "GET API KEY: https://sm.ms"\n'
                '}')
    qsconfig = {}


def pre_check(funcName: str, ext=True):
    try:
        api_key = qsconfig[funcName]
        if not api_key:
            exit('You should set %s api key at: %s' % (funcName, user_root + dir_char + '.qsrc'))
    except KeyError:
        if ext:
            exit('You should set %s api key at: %s' % (funcName, user_root + dir_char + '.qsrc'))
        else:
            return False
    else:
        return api_key
