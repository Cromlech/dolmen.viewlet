# -*- coding: utf-8 -*-

try:
    import martian
    from grokcore.security import require, util
    from dolmen import viewlet
    from cromlech.browser.interfaces import IRenderer, IViewSlot

    class ViewletSecurityGrokker(martian.ClassGrokker):
        martian.component(viewlet.Viewlet)
        martian.directive(require, default='zope.Public', name='permission')

        def execute(self, factory, config, permission, **kw):
            # we can also check here for ISecuredItem
            for method_name in IRenderer:
                config.action(
                    discriminator=('protectName', factory, method_name),
                    callable=util.protect_getattr,
                    args=(factory, method_name, permission))
            return True

    class ViewletManagerSecurityGrokker(ViewletSecurityGrokker):
        martian.component(viewlet.ViewletManager)

except ImportError:
    pass
