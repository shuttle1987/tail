from setuptools import  setup

setup(
    name='python-tail',
    description='Python implementation of UNIX tail command',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Click',
    ],
)
