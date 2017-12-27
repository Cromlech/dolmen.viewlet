# -*- coding: utf-8 -*-


from cromlech.browser import slot
from cromlech.security import IProtectedComponent, Forbidden
from dolmen.viewlet import viewlet_manager, viewlet, order
from dolmen.viewlet import ViewletManager, Viewlet
from zope.interface import implementer


@viewlet_manager
class Header(ViewletManager):
    pass


@viewlet
@order(3)
@slot(Header)
class HeaderBaseline(Viewlet):

    def render(self):
        return u"Baseline"


@viewlet
@order(1)
@slot(Header)
class Logo(Viewlet):

    def render(self):
        return u"A nice logo"


@viewlet
@order(2)
@slot(Header)
@implementer(IProtectedComponent)
class Private(Viewlet):

    allowed = frozenset(('admin@example.com', 'john@example.com'))

    def render(self):
        return u"You are allowed."

    def __check_security__(self, interaction):
        for principal in interaction.principals:
            if principal.id in self.allowed:
                continue
            else:
                return Forbidden(u"%r, you are not allowed" % principal.id)
        return None
