# -*- coding: utf-8 -*-
"""dolmen.viewlet tests
"""

import crom
from crom import testing
from crom.implicit import implicit
from cromlech.browser import IView, IViewSlot
from cromlech.browser.testing import TestRequest as Request, TestView as View
from dolmen.viewlet import IViewlet, IViewletManager, Viewlet, ViewletManager
from zope.interface.verify import verifyClass
from cromlech.security import ContextualInteraction, ContextualSecurityGuards
from cromlech.security import Principal, security_check


class Template(object):
    """A template mockup.
    """
    def render(self, renderer, *args, **kws):
        return "A simple template for %s." % renderer.__class__.__name__


class Context(object):
    pass


context = Context
request = Request()


def setup_function(method):
    testing.setup()


def teardown_function(method):
    testing.teardown()


def test_classes_integrity():
    assert verifyClass(IViewlet, Viewlet) is True
    assert verifyClass(IViewletManager, ViewletManager) is True


def test_manager_viewlet():
    """The manager is a location (a slot) where viewlet will display.
    It supervises the rendering of each viewlet and merged the output.
    """
    from .fixtures import entities as module

    # grok the component module
    crom.configure(module)

    # We define the actors
    mammoth = object()
    request = Request()
    view = View(mammoth, request)
    generic_template = Template()

    # module contains a manager, called 'Header'
    # we should retrieve it here
    manager = IViewSlot.adapt(mammoth, request, view, name='header')
    assert isinstance(manager, module.Header)

    with ContextualSecurityGuards(None, security_check):

        # Rending our manager should give us 1 viewlet.
        # The reason is : there's no interaction, therefore
        # protected viewlets are not computed.
        manager.update()
        rendering = manager.render()
        assert rendering == "A nice logo\nBaseline"

        # With an interaction, we should have a security context
        # With a wrong user, the viewlet is not retrieved.
        with ContextualInteraction(Principal('meaninglessguy@example.com')):
            manager.update()
            rendering = manager.render()
            assert rendering == "A nice logo\nBaseline"

        # With an interaction, we should have a security context
        # With a wrong user, the viewlet is not retrieved.
        with ContextualInteraction(Principal('admin@example.com')):
            manager.update()
            rendering = manager.render()
            assert rendering == "A nice logo\nYou are allowed.\nBaseline"
