# -*- coding: utf-8 -*-


from cromlech.browser import slot
from cromlech.security import ISecuredComponent, Forbidden
from dolmen.viewlet import viewlet_manager, viewlet, order
from dolmen.viewlet import ViewletManager, Viewlet
from zope.interface import implements



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
class Private(Viewlet):
    implements(ISecuredComponent)

    allowed = frozenset(('admin@example.com', 'john@example.com'))

    def render(self):
        return u"You are allowed."

    def __check__(self, interaction):
        for protagonist in interaction:
            username = protagonist.principal.id
            if username in self.allowed:
                continue
            else:
                return Forbidden(u"%r, you are not allowed" % username)
        return None
