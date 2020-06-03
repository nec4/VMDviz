from setuptools import setup, find_packages
from setuptools.command.install import install
import os

NAME = 'vmdviz'
VERSION = '0.0'

class InstallScript(install):
    def run(self):
        install.run(self)
        os.system('chmod u+x scripts/gen_rc.py')
        os.system('scripts/gen_rc.py')

def read(filename):
    import os
    BASE_DIR = os.path.dirname(__file__)
    filename = os.path.join(BASE_DIR, filename)
    with open(filename, 'r') as fi:
        return fi.read()

def readlist(filename):
    rows = read(filename).split("\n")
    rows = [x.strip() for x in rows if x.strip()]
    return list(rows)

setup(
    name=NAME,
    version=VERSION,
    author="Nick Charron",
    author_email="charron.nicholas.e@gmail.com",
    url='https://github.com/nec4/vmdviz',
    license='MIT',
    packages=find_packages(),
    zip_safe=True,
    cmdclass={
        'install': InstallScript
    },
    entry_points={
        'console_scripts': [
            'vmdviz_render = vmdviz.bin.vmdviz_render:main',
            'movie_combine = vmdviz.bin.movie_combine:main'
        ],
    },
    scripts = [
        'scripts/tachyon_movie.sh'
    ]
    )
