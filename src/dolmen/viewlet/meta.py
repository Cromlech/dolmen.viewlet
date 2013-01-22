# -*- coding: utf-8 -*-

from .interfaces import IViewletManager, IViewlet
from crom import target, name, registry
from cromlech.browser import IView, IRequest, request, context, view, slot
from grokker import grokker, directive, validator
from zope.interface import Interface


@grokker
@directive(context)
@directive(request)
@directive(target)
@directive(name)
@directive(registry)
def viewlet_manager_component(
        scanner, pyname, obj, registry,
        context=Interface, request=IRequest,
        view=IView, provides=IViewletManager, name=None):

    if name is None:
        name = obj.__name__.lower()

    obj.__component_name__ = name

    assert provides.isOrExtends(IViewletManager)

    def register():
        registry.register((context, request, view), target, name, obj)

    scanner.config.action(
        callable=register
        discriminator=('viewletManager',
                       context, request, view, name, registry))


@grokker
@directive(context)
@directive(request)
@directive(view)
@directive(slot)
@directive(target)
@directive(name)
@directive(registry)
def viewlet_component(
        scanner, pyname, obj, registry,
        context=Interface, request=IRequest,
        view=IView, slot=IViewletManager, provides=IViewlet, name=None):

    if name is None:
        name = obj.__name__.lower()

    obj.__component_name__ = name

    assert provides.isOrExtends(IViewlet)

    def register():
        registry.register((context, request, view, slot), target, name, obj)

    scanner.config.action(
        callable=register
        discriminator=('viewlet',
                       context, request, view, slot, name, registry))
