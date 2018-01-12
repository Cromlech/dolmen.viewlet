# -*- coding: utf-8 -*-
"""dolmen.viewlet tests
"""

import crom
import pytest

from crom import testing
from crom.implicit import implicit
from cromlech.browser import IView, IViewSlot
from cromlech.browser.testing import TestRequest as Request, TestView as View
from cromlech.security import ContextualInteraction, ContextualSecurityGuards
from cromlech.security import Principal, security_check
from cromlech.security.errors import MissingSecurityContext
from dolmen.viewlet import IViewlet, IViewletManager, Viewlet, ViewletManager
from zope.interface.verify import verifyClass


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

    # With no security guards in place, we can render the manager
    manager.update()
    rendering = manager.render()
    assert rendering == "A nice logo\nYou are allowed.\nBaseline"


    with ContextualSecurityGuards(None, security_check):
        
        # Rending our manager will fail.
        # The reason is : there's no interaction but security
        # guards are declared. Therefore, the security computation
        # cannot go further:
        with pytest.raises(MissingSecurityContext):
            manager.update()

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
