#!/usr/bin/env python3
from setuptools import setup, find_packages
from choo import __version__
setup(
    name='choo',
    packages=find_packages(),
    py_modules=['choo.choo', 'choo.networks'],
    version=__version__,
    description='uniform interface for public transport APIs',
    author='Nils Martin Klünder',
    author_email='choo@nomoketo.de',
    url='https://github.com/NoMoKeTo/choo',
    install_requires=['requests'],
    license='Apache License 2.0',
    scripts=['choo/choo-cli', 'choo/choo-server'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Internet'],
    include_package_data=True
)