import scraperwiki

scraperwiki.sqlite.attach("uk_lottery_scrapedownload_1")

def grants_by_month(la):
    l = scraperwiki.sqlite.select(u'SUM(`Grant amount`) AS amount, date(`Grant date`,"start of month") AS date_month_start FROM uk_lottery_scrapedownload_1.swdata WHERE `Local authority` = "%s" GROUP BY date(`Grant date`,"start of month")'%la)
    return dict((d[u'date_month_start'],d[u'amount']) for d in l)
        

print str(grants_by_month(u'Liverpool'))
import scraperwiki

scraperwiki.sqlite.attach("uk_lottery_scrapedownload_1")

def grants_by_month(la):
    l = scraperwiki.sqlite.select(u'SUM(`Grant amount`) AS amount, date(`Grant date`,"start of month") AS date_month_start FROM uk_lottery_scrapedownload_1.swdata WHERE `Local authority` = "%s" GROUP BY date(`Grant date`,"start of month")'%la)
    return dict((d[u'date_month_start'],d[u'amount']) for d in l)
        

print str(grants_by_month(u'Liverpool'))
