dolmen.viewlet
**************

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

  >>> class LeftColumn(ViewletManager):
  ...     pass

  >>> LeftColumn.__name__
  None

  >>> testing.grok_component('left', LeftColumn)
  True

  >>> LeftColumn.__name__
  leftcolumn

  >>> left = LeftColumn(mammoth, request, view)
  >>> left.render()
  ''

  >>> LeftColumn.template = generic_template
  >>> left.render()
  ''


Exemple component
=================

  >>> class WeatherBlock(dolmen.layout.Viewlet):
  ...     dolmen.layout.manager(LeftColumn)
  
  >>> testing.grok_component('weather', WeatherBlock)
