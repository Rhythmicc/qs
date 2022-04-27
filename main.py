import os
from QuickStart_Rhy import remove, dir_char
from QuickProject.Commander import Commander

app = Commander()


@app.command()
def upload():
    remove('dist')
    if os.system('python3 setup.py sdist'):
        os.system('python setup.py sdist')
    os.system('twine upload dist%s*' % dir_char)


@app.command()
def post(path: str):
    os.system(f'Qpro scp {path}')


@app.command()
def get(path: str):
    os.system(f'Qpro get {path}')


if __name__ == '__main__':
    app()
