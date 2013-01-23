# -*- coding: utf-8 -*-

import crom
from .interfaces import IViewletManager, IViewlet
from cromlech.browser import directives
from cromlech.browser import IView, IRequest
from grokker import grokker, directive, validator
from zope.interface import Interface


@grokker
@directive(directives.context)
@directive(directives.request)
@directive(crom.target)
@directive(crom.name)
@directive(crom.registry)
def viewlet_manager(
        scanner, pyname, obj, registry,
        context=Interface, request=IRequest,
        view=IView, target=IViewletManager, name=None):

    if name is None:
        name = obj.__name__.lower()

    obj.__component_name__ = name

    assert target.isOrExtends(IViewletManager)

    def register():
        registry.register((context, request, view), target, name, obj)

    scanner.config.action(
        callable=register,
        discriminator=('viewletManager',
                       context, request, view, name, registry))


@grokker
@directive(directives.context)
@directive(directives.request)
@directive(directives.view)
@directive(directives.slot)
@directive(crom.target)
@directive(crom.name)
@directive(crom.registry)
def viewlet(
        scanner, pyname, obj, registry,
        context=Interface, request=IRequest,
        view=IView, slot=IViewletManager, target=IViewlet, name=None):

    if name is None:
        name = obj.__name__.lower()

    obj.__component_name__ = name

    assert target.isOrExtends(IViewlet)

    def register():
        registry.register((context, request, view, slot), target, name, obj)

    scanner.config.action(
        callable=register,
        discriminator=('viewlet',
                       context, request, view, slot, name, registry))
