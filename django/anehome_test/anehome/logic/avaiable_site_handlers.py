from anehome_test.anehome.logic.snap.site_handler_globus      import SiteHandlerGlobus
from anehome_test.anehome.logic.snap.site_handler_perekrestok import SiteHandlerPerekrestok
from anehome_test.anehome.logic.snap.site_handler_okey        import SiteHandlerOkey
from anehome_test.anehome.logic.snap.site_handler_utkonos     import SiteHandlerUtkonos
from anehome_test.anehome.logic.snap.site_handler_gks         import SiteHandlerGks


SITE_HANDLERS = []
SITE_CODE_TO_HANDLER = {}


def init_site_handlers():
    global SITE_HANDLERS
    SITE_HANDLERS.append(SiteHandlerGlobus())
    SITE_HANDLERS.append(SiteHandlerPerekrestok())
    SITE_HANDLERS.append(SiteHandlerOkey())
    SITE_HANDLERS.append(SiteHandlerUtkonos())

    SITE_HANDLERS.append(SiteHandlerGks())

    for handler in SITE_HANDLERS:
        SITE_CODE_TO_HANDLER[handler.site_code] = handler
