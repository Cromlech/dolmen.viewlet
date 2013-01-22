# -*- coding: utf-8 -*-

from cromlech.browser import IView, IRequest, sort_components
from cromlech.i18n import getLanguage
from dolmen.viewlet import IViewletManager, IViewlet
from grokcore.component import baseclass, implements
from grokcore.component.util import sort_components


try:
    import cromlech.security
    from cromlech.security import ISecuredComponent, getInteraction
    from zope.interface.interfaces import ComponentLookupError

    def CHECKER(component):
        try:
            checker = ISecuredComponent(component)
            interaction = getInteraction()
            error = checker.__checker__(interaction)
            if error is not None:
                return False
        except ComponentLookupError:
            pass
        return True

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
        for name, component in interface.all_components(
                context, request, view, collection):
            if CHECKER is not None and not CHECKER(component):
                continue

            component.update()
            if bool(component.available) is True:
                yield component

    assert interface.isOrExtends(IViewlet), "interface must extends IViewlet"
    assert IRequest.providedBy(request), "request must be an IRequest"
    return registry_components()


@security_wrapped
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
    return interface.adapt(context, request, view, name=name)


def aggregate_views(views):
    """Aggregates a given list of IView components.
    """
    return u'\n'.join([view.render() for view in views])


class ViewletManager(object):
    """A collection of viewlet components.
    A viewlet manager is a manager meant to be used at a view level.
    """
    implements(IViewletManager)

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
    def target_language(self):
        return getLanguage()

    def update(self, *args, **kwargs):
        self.viewlets = sort_components(list(query_components(
            self.context, self.request, self.view, self, interface=IViewlet)))

    def render(self, *args, **kwargs):
        if self.template is None:
            return self.aggregate(self.viewlets)
        return self.template.render(
           self, target_language=self.target_language, **self.namespace())


class Viewlet(object):
    """A renderable component, part of a collection.
    A viewlet is to be used at a view level.
    """
    implements(IViewlet)

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
    def target_language(self):
        return getLanguage()

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
            self, target_language=self.target_language, **self.namespace())
