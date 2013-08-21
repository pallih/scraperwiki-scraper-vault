import scraperwiki

scraperwiki.utils.httpresponseheader("Content-Disposition", "inline; filename=foo")
scraperwiki.utils.httpresponseheader("Content-Disposition", "inline; filename=«silly»")
