# -*- coding: utf-8 -*-

import doctest
import unittest
import dolmen.viewlet
from zope.component.testlayer import ZCMLFileLayer

FLAGS = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
layer = ZCMLFileLayer(dolmen.viewlet.tests)


def test_suite():
    """Get a testsuite of all doctests.
    """
    suite = unittest.TestSuite()
    for name in ['security.txt']:
        test = doctest.DocFileSuite(
            name,
            package=dolmen.viewlet.tests,
            optionflags=FLAGS,
            )
        suite.addTest(test)
    suite.layer = layer
    return suite
