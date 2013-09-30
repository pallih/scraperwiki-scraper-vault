import scraperwiki
scraperwiki.sqlite.attach("fumixs_email_alert_scraper")
data = scraperwiki.sqlite.select(
    '''* from fumixs_email_alert_scraper.swdata 
    order by title desc'''
)
for d in data:
    print "<a href='", d["link"],"' alt='",d["title"],"'>"
    print "<img src='", d["thumbnail"], "' />"
    print "</a>"import scraperwiki
scraperwiki.sqlite.attach("fumixs_email_alert_scraper")
data = scraperwiki.sqlite.select(
    '''* from fumixs_email_alert_scraper.swdata 
    order by title desc'''
)
for d in data:
    print "<a href='", d["link"],"' alt='",d["title"],"'>"
    print "<img src='", d["thumbnail"], "' />"
    print "</a>"