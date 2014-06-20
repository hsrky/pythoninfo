#!/usr/bin/env python
# coding: utf-8

from distutils.core import setup

setup (
  name = 'pythoninfo',
  packages = ['pythoninfo'],
  package_dir = {'pythoninfo': 'pythoninfo'},
  version = '0.0.1',
  author = 'ky lee',
  author_email = 'ky.github@outlook.com',
  description = 'Python environment information for debugging',
  long_description= open('README.md').read(),
  url = 'https://github.com/hsrky/pythoninfo/',
  download_url = '',
  license = 'LICENSE.txt',
  keywords = ['debugging', 'testing'],
)