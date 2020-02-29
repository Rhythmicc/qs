import requests
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
                '}')
    qsconfig = {}


def rmbg(filePath: str):
    try:
        api_key = qsconfig['rmbg']
        if not api_key:
            exit('You should set rmbg api key at: %s' % (user_root + dir_char + '.qsrc'))
    except KeyError:
        exit('You should set rmbg api key at: %s' % (user_root + dir_char + '.qsrc'))
    else:
        res = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': open(filePath, 'rb')},
            data={'size': 'auto'},
            headers={'X-Api-Key': api_key},
        )
        if res.status_code == requests.codes.ok:
            img_name = filePath.split(dir_char)[-1].split('.')[0]
            if dir_char in filePath:
                img_root = dir_char.join(filePath.split(dir_char)[:-1]) + dir_char
            else:
                img_root = ''
            with open(img_root + img_name + '_rmbg.png', 'wb') as f:
                f.write(res.content)
        else:
            print('ERROR:', res.status_code, res.text)
