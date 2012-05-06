# -*- coding: utf-8 -*-

import martian
import dolmen.viewlet
from dolmen.viewlet import IViewletManager, IViewlet
from zope.interface import Interface
from zope.component import provideAdapter


def get_default_name(factory, module=None, **data):
    return factory.__name__.lower()


class ViewletManagerGrokker(martian.ClassGrokker):
    martian.component(dolmen.viewlet.ViewletManager)
    martian.directive(dolmen.viewlet.context, default=Interface)
    martian.directive(dolmen.viewlet.request, default=Interface)
    martian.directive(dolmen.viewlet.view)
    martian.directive(dolmen.viewlet.provides, default=IViewletManager)
    martian.directive(dolmen.viewlet.name, get_default=get_default_name)

    def execute(self, factory, config,
                context, request, view, provides, name, **kw):
        assert provides.isOrExtends(IViewletManager)
        factory.__component_name__ = name
        config.action(
            discriminator=('viewletManager', context, request, view, name),
            callable=provideAdapter,
            args=(factory, (context, request, view), IViewletManager, name))
        return True


class ViewletGrokker(martian.ClassGrokker):
    martian.component(dolmen.viewlet.Viewlet)
    martian.directive(dolmen.viewlet.context, default=Interface)
    martian.directive(dolmen.viewlet.request, default=Interface)
    martian.directive(dolmen.viewlet.view)
    martian.directive(dolmen.viewlet.slot)
    martian.directive(dolmen.viewlet.provides, default=IViewlet)
    martian.directive(dolmen.viewlet.name, get_default=get_default_name)

    def execute(self, factory, config,
                context, request, view, slot, provides, name, **kw):
        assert provides.isOrExtends(IViewlet)
        factory.__component_name__ = name
        config.action(
            discriminator=(
                'viewlet', context, request, view, slot, name),
            callable=provideAdapter,
            args=(factory, (context, request, view, slot),
                  provides, name))
        return True
