from os import path
from setuptools import setup
from pyauto import __version__


with open(path.join(path.dirname(__file__), 'requirements.txt')) as f:
    reqs = [l for l in f.read().strip().split('\n') if not l.startswith('-')]

setup(
    name='PACKAGE',
    version=__version__,
    description='WHAT',
    author='WHO',
    packages=['PACKAGE'],
    package_dir={'PACKAGE': 'PACKAGE'},
    install_requires=reqs,
    url='https://github.com/USER/PACKAGE',
)
