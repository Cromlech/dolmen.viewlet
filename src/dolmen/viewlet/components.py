# -*- coding: utf-8 -*-

from .interfaces import IViewletManager, IViewlet
from crom import ComponentLookupError
from cromlech.browser import IView, IRequest, sort_components
from cromlech.i18n import getLocalizer
from zope.interface import implementer

try:
    from cromlech.security import getSecurityGuards

except ImportError:

    def getSecurityGuards():
        return None, None


def query_components(context, request, view, collection, interface=IViewlet):
    """Query components of the given collection :

    * Queries the registry according to context, request, view, manager.
    * Updates the components.
    * Filters out the unavailable components.
    * Returns an iterable of components.
    """
    def registry_components():
        security_predict, security_check = getSecurityGuards()
        
        for name, factory in interface.all_components(
                context, request, view, collection):

            if security_predict is not None:
                factory = security_predict(factory, swallow_errors=True)

            if factory is not None:
                component = factory(context, request, view, collection)
                if security_check is not None:
                    component = security_check(component, swallow_errors=True)

                if component is not None:
                    component.update()
                    if bool(component.available) is True:
                        yield component

    assert interface.isOrExtends(IViewlet), "interface must extends IViewlet"
    assert IRequest.providedBy(request), "request must be an IRequest"
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
    assert IRequest.providedBy(request), "request must be an IRequest"

    security_predict, security_check = getSecurityGuards()
    try:
        factory = interface.component(context, request, view, name=name)
        if factory is not None and security_predict is not None:
            factory = security_predict(factory)  # raises if security error
            manager = factory(context, request, view)
            if security_check is not None:
                manager = security_check(manager)  # raises if security error
    except ComponentLookupError:
        pass
    else:
        return manager


def aggregate_views(views):
    """Aggregates a given list of IView components.
    """
    return u'\n'.join([view.render() for view in views])


@implementer(IViewletManager)
class ViewletManager(object):
    """A collection of viewlet components.
    A viewlet manager is a manager meant to be used at a view level.
    """

    template = None

    @property
    def __name__(self):
        return getattr(self, '__component_name__', None)

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.view = view
        self.viewlets = []
        self.__parent__ = view

    def namespace(self):
        return {
            'context': self.context,
            'request': self.request,
            'view': self.view,
            'manager': self,
            }

    def aggregate(self, viewlets):
        return aggregate_views(viewlets)

    @property
    def translate(self):
        localizer = getLocalizer()
        if localizer is not None:
            return localizer.translate
        return None

    def update(self, *args, **kwargs):
        self.viewlets = sort_components(list(query_components(
            self.context, self.request, self.view, self, interface=IViewlet)))

    def render(self, *args, **kwargs):
        if self.template is None:
            return self.aggregate(self.viewlets)
        return self.template.render(
           self, translate=self.translate, **self.namespace())


@implementer(IViewlet)
class Viewlet(object):
    """A renderable component, part of a collection.
    A viewlet is to be used at a view level.
    """
    template = None
    available = True

    @property
    def __name__(self):
        return getattr(self, '__component_name__', None)

    def __init__(self, context, request, view, manager):
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager
        self.__parent__ = manager

    def namespace(self):
        return {
            'context': self.context,
            'request': self.request,
            'view': self.view,
            'manager': self.manager,
            'viewlet': self,
            }

    @property
    def translate(self):
        localizer = getLocalizer()
        if localizer is not None:
            return localizer.translate
        return None

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
        return self.template.render(
            self, translate=self.translate, **self.namespace())
