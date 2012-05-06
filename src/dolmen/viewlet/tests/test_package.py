# -*- coding: utf-8 -*-
"""dolmen.viewlet tests
"""
import dolmen.viewlet

from cromlech.browser.interfaces import IViewSlot
from cromlech.browser.testing import TestView, TestRequest
from grokcore.security import require
from zope.component import getMultiAdapter
from zope.interface import implements, classProvides
from zope.interface.verify import verifyClass, verifyObject
from zope.location import ILocation
from zope.security.interfaces import IInteraction, ISecurityPolicy
from zope.security.management import newInteraction, endInteraction
from zope.security.management import setSecurityPolicy, getSecurityPolicy
from zope.security.simplepolicies import ParanoidSecurityPolicy
from zope.security.testing import Principal, Participation
from zope.security.checker import ProxyFactory, Unauthorized

import pytest
from dolmen.viewlet import testing
from grokcore.component.testing import grok_component
from zope.component.testlayer import ZCMLFileLayer
from zope.testing.cleanup import cleanUp

layer = ZCMLFileLayer(dolmen.viewlet.tests)


class TestPolicy(ParanoidSecurityPolicy):

    def checkPermission(self, permission, object):
        if permission == "zope.Public":
            return True

        for p in self.participations:
            if (permission == 'zope.ManageContent' and
                p.principal.id == 'Master'):
                return True
        return False


def setup_module(module):
    layer.setUp()
    testing.grok('dolmen.viewlet.tests.test_package')
    assert setSecurityPolicy(TestPolicy)


def teardown_module(module):
    layer.tearDown()
    cleanUp()


class Template(object):
    """A template mockup.
    """
    def render(self, renderer, *args, **kws):
        return "A simple template for %s." % renderer.__class__.__name__


class Header(dolmen.viewlet.ViewletManager):
    pass


class Logo(dolmen.viewlet.Viewlet):
    dolmen.viewlet.slot(Header)

    def render(self):
        return u"A nice logo"


class Breadcrumb(dolmen.viewlet.Viewlet):
    dolmen.viewlet.slot(Header)
    require('zope.ManageContent')

    def render(self):
        return u"You are here > www > cromlech > viewlet"


def test_classes_integrity():

    assert verifyClass(dolmen.viewlet.IViewlet,
                       dolmen.viewlet.Viewlet) is True

    assert verifyClass(dolmen.viewlet.IViewletManager,
                       dolmen.viewlet.ViewletManager) is True


def test_manager_viewlet():
    """The manager is a location (a slot) where viewlet will display.
    It supervises the rendering of each viewlet and merged the output.
    """
    # We define the actors
    mammoth = object()
    request = TestRequest()
    view = TestView(mammoth, request)
    generic_template = Template()

    class LeftColumn(dolmen.viewlet.ViewletManager):
        pass

    assert not getattr(LeftColumn, '__component_name__', None)
    assert grok_component('left', LeftColumn) is True
    assert getattr(LeftColumn, '__component_name__') == 'leftcolumn'

    # We instanciate, verify and try to render
    left = LeftColumn(mammoth, request, view)
    assert verifyObject(dolmen.viewlet.IViewletManager, left)

    left.update()
    assert left.render() == u''

    manager = getMultiAdapter((mammoth, request, view),
                              IViewSlot, name='leftcolumn')
    assert manager.__class__ == LeftColumn

    manager = dolmen.viewlet.query_viewlet_manager(view, name='leftcolumn')
    assert manager.__class__ == LeftColumn

    left.template = generic_template
    left.update()
    assert left.render() == 'A simple template for LeftColumn.'

    # We now assign a viewlet to our manager
    class WeatherBlock(dolmen.viewlet.Viewlet):
        require('zope.Public')
        dolmen.viewlet.slot(LeftColumn)

    assert dolmen.viewlet.IViewlet.implementedBy(WeatherBlock) is True
    assert grok_component('weather', WeatherBlock) is True

    newInteraction(Participation(Principal('User')))

    left.template = None
    left.update()

    assert len(list(dolmen.viewlet.query_components(
      mammoth, request, view, left))) == 1

    assert manager.__class__ == LeftColumn
    assert len(left.viewlets) == 1

    # A manager should be a valid ILocation
    assert ILocation.providedBy(manager)
    assert manager.__parent__ == view
    assert manager.__name__ == 'leftcolumn'

    # We need a template defined or it fails.
    with pytest.raises(NotImplementedError) as e:
        left.update()
        left.render()

    assert str(e.value) == (
        "<class 'dolmen.viewlet.tests.test_package.WeatherBlock'> : "
        "Provide a template or override the render method")

    # We now define a template
    WeatherBlock.template = generic_template
    left.update()
    assert left.render() == u'A simple template for WeatherBlock.'

    # Let's register another viewlet
    class AnotherBlock(dolmen.viewlet.Viewlet):
        require('zope.ManageContent')
        dolmen.viewlet.slot(LeftColumn)
        template = generic_template

    assert grok_component('another', AnotherBlock)
    left.update()
    assert left.render() == u'A simple template for WeatherBlock.'

    # A viewlet should be a valid ILocation
    viewlet = left.viewlets[0]
    assert ILocation.providedBy(viewlet)
    assert viewlet.__parent__.__class__ == LeftColumn
    assert viewlet.__name__ == 'weatherblock'

    endInteraction()

    newInteraction(Participation(Principal('Master')))

    left.update()
    assert left.render() == (u'A simple template for AnotherBlock.\n'
                      u'A simple template for WeatherBlock.')

    # We should be able to set an order
    dolmen.viewlet.order.set(AnotherBlock, (10, 10))
    left.update()
    assert left.render() == (u'A simple template for WeatherBlock.\n'
                             u'A simple template for AnotherBlock.')

    endInteraction()


    # Let's register a secured viewlet manage
    class Secured(dolmen.viewlet.ViewletManager):
        require('zope.ManageContent')

    assert grok_component('secured', Secured) is True

    newInteraction(Participation(Principal('User')))

    # We instanciate, verify and try to render
    secured = ProxyFactory(Secured(mammoth, request, view))
    with pytest.raises(Unauthorized):
        secured.update()

    endInteraction()


    newInteraction(Participation(Principal('Master')))

    # We instanciate, verify and try to render
    secured.update()
    assert secured.render() == u''

    endInteraction()
