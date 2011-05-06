# -*- coding: utf-8 -*-

from zope.component import getAdapters, getMultiAdapter
from cromlech.io import IRequest
from cromlech.browser import IView
from dolmen.viewlet import IViewletManager, IViewlet
from grokcore.component import baseclass, implements
from grokcore.component.util import sort_components

try:
    import zope.security

    def check_security(component, attribute):
        try:
            return zope.security.canAccess(component, attribute)
        except zope.security.interfaces.Forbidden:
            return False

    CHECKER = check_security
except ImportError:
    CHECKER = None


def query_components(context, request, view, collection, interface=IViewlet):
    """Query components of the given collection :

    * Queries the registry according to context, request, view, manager.
    * Updates the components.
    * Filters out the unavailable components.
    * Returns an iterable of components.
    """

    def registry_components():
        for name, component in getAdapters(
            (context, request, view, collection), interface):

            if CHECKER is not None and not CHECKER(component, 'render'):
                continue

            component.update()
            if bool(component.available) is True:
                yield component

    assert interface.isOrExtends(IViewlet), "interface must extends IViewlet"
    assert IRequest.providedBy(request), "request must implements IRequest"
    assert IView.providedBy(view), "view must implements IView"
    return registry_components()


def query_viewlet_manager(view, context=None, request=None,
                          interface=IViewletManager, name=''):
    """Retrieve a viewlet manager"""
    assert IView.providedBy(view), "view must implements IView"
    if context is None:
        context = view.context
    if request is None:
        request = view.request
    assert interface.isOrExtends(IViewletManager), (
                                    "interface must extends IViewletManager")
    assert IRequest.providedBy(request), "request must implements IRequest"
    return getMultiAdapter((context, request, view), interface, name)


def aggregate_views(views):
    """Aggregates a given list of IView components.
    """
    return u'\n'.join([view.render() for view in views])


class ViewletManager(object):
    """A collection of viewlet components.
    A viewlet manager is a manager meant to be used at a view level.
    """
    baseclass()
    implements(IViewletManager)

    template = None

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.view = view
        self.viewlets = []

    def namespace(self):
        return {
            'context': self.context,
            'request': self.request,
            'view': self.view,
            'manager': self,
            }

    def aggregate(self, viewlets):
        return aggregate_views(viewlets)

    def update(self, *args, **kwargs):
        self.viewlets = sort_components(list(query_components(
            self.context, self.request, self.view, self, interface=IViewlet)))

    def render(self, *args, **kwargs):
        if self.template is None:
            return self.aggregate(self.viewlets)
        return self.template.render(self)

    def __call__(self, *args, **kwargs):
        """Update and render"""
        self.update(*args, **kwargs)
        return self.render(*args, **kwargs)


class Viewlet(object):
    """A renderable component, part of a collection.
    A viewlet is to be used at a view level.
    """
    baseclass()
    implements(IViewlet)

    template = None
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

    def update(self, *args, **kwargs):
        # Can be overriden easily.
        pass

    def render(self, *args, **kwargs):
        # Override if you need to return anything not
        # as simple as a unique unconditional template.
        if self.template is None:
            raise NotImplementedError(
                '%r : Provide a template or override the render method' %
                self.__class__)
        return self.template.render(self)
