# -*- coding: utf-8 -*-

from zope.configuration.config import ConfigurationMachine
from grokcore.component import zcml


def grok(*modules):
    config = ConfigurationMachine()
    zcml.do_grok('grokcore.component.meta', config)
    zcml.do_grok('dolmen.viewlet.meta', config)
    for name in modules:
        zcml.do_grok(name, config)
    config.execute_actions()
