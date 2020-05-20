# -*- coding: utf-8 -*-

import io
import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
DESCRIPTION = 'A fake server than catch all path and response success message or whatever data you defined.'


try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except Exception:
    long_description = DESCRIPTION


def read(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read()


setup(
    name='fake-server',
    version='0.1',
    author="chroming",
    author_email="chroming@live.com",
    url='https://github.com/chroming/fake_server',
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['fake_server'],
    install_requires=[
        'click==7.1.2',
        'flask==1.1.2',
        'gunicorn'
    ],
    entry_points='''
        [console_scripts]
        fake-server=fake_server:fake_server
    ''',
)