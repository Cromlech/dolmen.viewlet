dolmen.viewlet
**************

  >>> import dolmen.viewlet
  >>> dolmen.viewlet.testing.grok('dolmen.viewlet.meta')

Test environnment
=================

  >>> mammoth = object()
  >>> request = object()
  >>> view = object()

  >>> class Template(object):
  ...     def render(self, renderer):
  ...         return "A simple template for %r." % renderer

  >>> generic_template = Template()


Example manager
===============

  >>> import dolmen.viewlet
  >>> from grokcore.component import testing

  >>> class LeftColumn(dolmen.viewlet.ViewletManager):
  ...     pass

  >>> LeftColumn.__name__
  'LeftColumn'

  >>> testing.grok_component('left', LeftColumn)
  True

  >>> LeftColumn.__name__
  'leftcolumn'

  >>> left = LeftColumn(mammoth, request, view)
  >>> left()
  u''

  >>> left.template = generic_template
  >>> left()
  'A simple template for <dolmen.viewlet.tests.leftcolumn object at ...>.'


Exemple component
=================

  >>> class WeatherBlock(dolmen.viewlet.Viewlet):
  ...     dolmen.viewlet.manager(LeftColumn)

  >>> testing.grok_component('weather', WeatherBlock)
  True

  >>> left.template = None
  >>> left.update()
  >>> print left.viewlets
  [<dolmen.viewlet.tests.weatherblock object at ...>]

  >>> left()
  Traceback (most recent call last):
  ...
  NotImplementedError: <class 'dolmen.viewlet.tests.weatherblock'> :
  Provide a template or override the render method

  >>> 
