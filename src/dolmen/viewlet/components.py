# -*- coding: utf-8 -*-

from zope.component import getAdapters
from cromlech.browser.interfaces import IComponent, IViewletManager, IViewlet
from grokcore.component import baseclass
from grokcore.component.util import sort_components


def query_components(context, request, view, collection, interface=IComponent):
    """Query components of the given collection :
    * Queries the registry according to context, request, view, manager.
    * Updates the components.
    * Filters out the unavailable components.
    * Returns an iterable of components.
    """
    def registry_components():
        for name, component in getAdapters(
            (context, request, view), interface):
            component.update()
            if bool(component.available) is True:
                yield component

    assert interface.isOrExtends(IComponent).
    return registry_components()


def aggregate_views(views):
    """Aggregates a given list of IView components.
    """
    return u'\n'.join([view.render() for view in views])


class ViewletManager(object):
    """A collection of viewlet components.
    A viewlet manager is a manager meant to be used at a view level.
    """
    baseclass()

    template = None
    __name__ = None
    aggregate = aggregate_views

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.view = view

    def namespace(self):
        return {
            'context': self.context,
            'request': self.request,
            'view': self.view,
            'manager': self,
            }

    def update(self):
        self.viewlets = sort_components(list(query_components(
            self.context, self.request, self.view, self, interface=IViewlet)))

    def render(self):
        if self.template is None:
            return self.aggregate(self.viewlets)
        return self.template.render(self)

    def __call__(self):
        return self.render()


class Viewlet(object):
    """A renderable component, part of a collection.
    A viewlet is to be used at a view level.
    """
    baseclass()

    template = None
    __name__ = None
    available = True

    def __init__(self, context, request, view, manager):
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager

    def namespace(self):
        return {
            'context': self.context,
            'request': self.request,
            'view': self.view,
            'manager': self.manager,
            'viewlet': self,
            }
    
    def update(self):
        # Can be overriden easily.
        pass

    def render(self):
        # Override if you need to return anything not
        # as simple as a unique unconditional template.
        if self.template is None:
            return NotImplementedError(
                '%r : Provide a template or override the render method' %
                self.__class__)
        return self.template.render(self)
