# -*- coding: utf-8 -*-

from zope.interface import Attribute
from cromlech.browser.interfaces import IRenderer


class IViewletManager(IRenderer):
    """compose a set of viewlet together and render in a more global view
    """
    context = Attribute("Object that the view presents.")
    request = Attribute("Request that the view was looked up with.")
    view = Attribute("View on which the manager is called.")
    viewlets = Attribute("A list of the components to aggregate.")


class IViewlet(IRenderer):
    """a viewlet is a component rendering a small part of the global view
    driven by a manager
    """
    context = Attribute("Object that the view presents.")
    request = Attribute("Request that the view was looked up with.")
    view = Attribute("View on which the manager is called.")
    manager = Attribute("Manager that aggregates the viewlets.")
