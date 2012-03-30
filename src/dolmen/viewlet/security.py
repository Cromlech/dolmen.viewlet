# -*- coding: utf-8 -*-

try:
    import martian
    import grokcore.security
    from dolmen import viewlet
    from cromlech.browser.interfaces import IRenderer, IViewSlot

    class ViewletSecurityGrokker(martian.ClassGrokker):
        martian.component(viewlet.Viewlet)
        martian.directive(grokcore.security.require, name='permission')

        def execute(self, factory, config, permission, **kw):
            # we can also check here for ISecuredItem
            for method_name in IRenderer:
                config.action(
                    discriminator=('protectName', factory, method_name),
                    callable=grokcore.security.util.protect_getattr,
                    args=(factory, method_name, permission),
                    )
            return True

    class ViewletManagerSecurityGrokker(ViewletSecurityGrokker):
        martian.component(viewlet.ViewletManager)

except ImportError:
    pass
