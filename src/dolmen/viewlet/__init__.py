# -*- coding: utf-8 -*-

# directives
from grokcore.component import context, name, provides, order
from cromlech.io.directives import request
from cromlech.browser.directives import view, slot

# interfaces
from dolmen.viewlet.interfaces import IViewlet, IViewletManager

# components
from dolmen.viewlet.components import ViewletManager, Viewlet
import dolmen.viewlet.testing
