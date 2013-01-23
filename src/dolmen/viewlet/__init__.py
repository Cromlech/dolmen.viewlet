# -*- coding: utf-8 -*-

# directives
from crom import name, target
from cromlech.browser.directives import view, slot, request, order, context

# interfaces
from .interfaces import IViewlet, IViewletManager

# components
from .components import ViewletManager, Viewlet
from .components import query_components, query_viewlet_manager

# grokkers
from .meta import viewlet_manager, viewlet
