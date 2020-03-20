basic_funcs = {
    'self': 'basic',
    '-u': 'u',
    '-a': 'open_app',
    '-f': 'open_file',
    '-i': 'init',
    '-time': 'cur_time',
}

system_funcs = {
    'self': 'system',
    '-top': 'top',
    '-mktar': 'mktar',
    '-untar': 'untar',
    '-mkzip': 'mkzip',
    '-unzip': 'unzip',
}

net_funcs = {
    'self': 'nettools',
    '-ftp': 'ftp',
    '-dl': 'download',
    '-upgrade': 'upgrade',
    '-upload': 'upload_pypi'
}

api_funcs = {
    'self': 'api',
    '-trans': 'translate',
    '-rmbg': 'remove_bg',
    '-smms': 'ImgBed',
    '-ali_oss': 'ali_oss',
    '-qiniu': 'qiniu',
    '-weather': 'weather',
}

image_funcs = {
    'self': 'imagedeal',
    '-stbg': 'set_img_background',
}