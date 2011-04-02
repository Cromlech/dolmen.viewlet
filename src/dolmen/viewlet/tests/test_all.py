# -*- coding: utf-8 -*-

import doctest
import unittest
import dolmen.viewlet

FLAGS = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


def test_suite():
    """Get a testsuite of all doctests.
    """
    suite = unittest.TestSuite()
    for name in ['../README.txt']:
        test = doctest.DocFileSuite(
            name,
            package=dolmen.viewlet.tests,
            globs=dict(__name__="dolmen.viewlet.tests"),
            optionflags=FLAGS,
            )
        suite.addTest(test)
    return suite
