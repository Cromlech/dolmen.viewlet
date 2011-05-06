# -*- coding: utf-8 -*-
"""dolmen.viewlet tests
"""
import dolmen.viewlet

from grokcore.security import require
from cromlech.browser.interfaces import IViewSlot
from cromlech.browser.testing import TestView
from cromlech.io.testing import TestRequest
from zope.interface.verify import verifyClass, verifyObject
from zope.component import getMultiAdapter
from zope.security.management import newInteraction, endInteraction
from zope.security.testing import Principal, Participation

import pytest
from dolmen.viewlet import testing
from grokcore.component.testing import grok_component
from zope.component.testlayer import ZCMLFileLayer
from zope.testing.cleanup import cleanUp

layer = ZCMLFileLayer(dolmen.viewlet.tests)


def setup_module(module):
    layer.setUp()
    testing.grok('dolmen.viewlet.tests.test_package')


def teardown_module(module):
    layer.tearDown()
    cleanUp()


class Template(object):
  """A template mockup.
  """
  def render(self, renderer):
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
    assert left() == u''

    manager = getMultiAdapter((mammoth, request, view),
                              IViewSlot, name='leftcolumn')
    assert manager.__class__ == LeftColumn

    manager = dolmen.viewlet.query_viewlet_manager(view, name='leftcolumn')
    assert manager.__class__ == LeftColumn


    left.template = generic_template
    assert left() == 'A simple template for LeftColumn.'


    # We now assign a viewlet to our manager
    class WeatherBlock(dolmen.viewlet.Viewlet):
        require('zope.Public')
        dolmen.viewlet.slot(LeftColumn)
  
    assert dolmen.viewlet.IViewlet.implementedBy(WeatherBlock) is True
    assert grok_component('weather', WeatherBlock) is True

    newInteraction(Participation(Principal('cromlech.user')))

    left.template = None
    left.update()

    assert len(list(dolmen.viewlet.query_components(
      mammoth, request, view, left))) == 1

    assert manager.__class__ == LeftColumn
    assert len(left.viewlets) == 1


    # We need a template defined or it fails.
    with pytest.raises(NotImplementedError) as e:
      left()

    assert str(e.value) == (
      "<class 'dolmen.viewlet.tests.test_package.WeatherBlock'> : "
      "Provide a template or override the render method")

    # We now define a template
    WeatherBlock.template = generic_template
    assert left() == u'A simple template for WeatherBlock.'


    # Let's register another viewlet
    class AnotherBlock(dolmen.viewlet.Viewlet):
        require('zope.ManageContent')
        dolmen.viewlet.slot(LeftColumn)
        template = generic_template

    assert grok_component('another', AnotherBlock)
    assert left() ==  u'A simple template for WeatherBlock.'

    endInteraction()

    newInteraction(Participation(Principal('cromlech.manager')))
    
    assert left() == (u'A simple template for AnotherBlock.\n'
                      u'A simple template for WeatherBlock.')

    # We should be able to set an order
    dolmen.viewlet.order.set(AnotherBlock, (10, 10))
    assert left() ==  (u'A simple template for WeatherBlock.\n'
                       u'A simple template for AnotherBlock.')

    endInteraction()