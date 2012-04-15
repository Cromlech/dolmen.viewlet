# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os.path import join

name = 'dolmen.viewlet'
version = '0.3'
readme = open('README.txt').read()
history = open(join('docs', 'HISTORY.txt')).read()

install_requires = [
    'cromlech.browser >= 0.3a2',
    'cromlech.i18n',
    'cromlech.io >= 0.2a1',
    'grokcore.component',
    'martian',
    'setuptools',
    'zope.component',
    'zope.interface',
    'zope.location',
    ]

tests_require = [
    'pytest',
    'cromlech.browser [test]',
    'zope.configuration',
    'zope.testing',
    ]

security_require = [
    'grokcore.security >= 1.5',
    'zope.security',
    ]

setup(name=name,
      version=version,
      description='Dolmen viewlets components',
      long_description=readme + '\n\n' + history,
      keywords='Cromlech Grok Dolmen Viewlet',
      author='Souheil Chelfouh',
      author_email='trollfot@gmail.com',
      url='',
      license='ZPL',
      classifiers=[
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        ],
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['dolmen'],
      include_package_data=True,
      platforms='Any',
      zip_safe=False,
      tests_require=tests_require,
      install_requires=install_requires,
      extras_require={
          'test': tests_require,
          'security': security_require,
          },
      )
