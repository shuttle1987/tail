from setuptools import  setup

setup(
    name='python-tail',
    description='Python implementation of UNIX tail command',
    version='0.1',
    packages=['tail'],
    install_requires=[
        'Click',
    ],
)
