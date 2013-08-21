import scraperwiki
import lxml.html

html = scraperwiki.scrape("https://networkhealth.bazaarvoice.com/nydus/health/etl")
scraperwiki.sqlite.save_var('status', html)

print html
