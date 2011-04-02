# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os.path import join

name = 'dolmen.viewlet'
version = '0.1'
readme = open(join('src', 'dolmen', 'viewlet', "README.txt")).read()
history = open(join('docs', 'HISTORY.txt')).read()

install_requires = [
    'setuptools',
    'martian',
    'grokcore.component',
    'cromlech.io',
    'cromlech.browser',
    ]

tests_require = [
    ]

setup(name = name,
      version = version,
      description = 'Dolmen viewlets components',
      long_description = readme + '\n\n' + history,
      keywords = 'Cromlech Grok Dolmen Viewlet',
      author = 'Souheil Chelfouh',
      author_email = 'trollfot@gmail.com',
      url = '',
      license = 'ZPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages = ['dolmen'],
      include_package_data = True,
      platforms = 'Any',
      zip_safe = False,
      tests_require = tests_require,
      install_requires = install_requires,
      extras_require = {'test': tests_require},
      classifiers = [
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        ],
      )
